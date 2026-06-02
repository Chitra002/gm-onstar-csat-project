"""
insight_summarizer.py
=====================
GM OnStar CSAT Improvement Project — AI Automation Module

Generates a plain-English weekly insight digest from aggregated CSAT metrics.
Output is ready to paste into an email or Teams message for leadership.

Prompt engineering approach:
  - Structured JSON data input keeps the prompt factual and grounded
  - Explicit output format instructions prevent hallucination
  - Role framing ensures business-appropriate tone
  - Iterative prompting: first generates findings, then recommendations

Usage:
    python src/ai_automation/insight_summarizer.py \
        --input data/processed/master_with_themes.csv \
        --week 2026-W22
"""

import os
import json
import argparse
import pandas as pd
import anthropic
from datetime import datetime, timedelta


MODEL = "claude-sonnet-4-20250514"


def compute_weekly_metrics(df: pd.DataFrame, week_str: str) -> dict:
    """
    Compute the weekly metrics summary that will be passed to the LLM.
    All computation is done in Python/pandas — the LLM only does interpretation.
    """
    df["ticket_closed_at"] = pd.to_datetime(df["ticket_closed_at"])
    df["iso_week"] = df["ticket_closed_at"].dt.strftime("%G-W%V")

    week_df = df[df["iso_week"] == week_str].copy()
    prev_week = (
        datetime.strptime(week_str + "-1", "%G-W%V-%u") - timedelta(weeks=1)
    ).strftime("%G-W%V")
    prev_df = df[df["iso_week"] == prev_week].copy()

    def safe_rate(num, denom):
        return round(num / denom * 100, 1) if denom > 0 else None

    # Current week metrics
    total     = len(week_df)
    sent      = int(week_df["survey_sent_flag"].sum())
    completed = int(week_df["survey_completed_flag"].sum())
    avg_csat  = round(week_df["csat_score"].mean(), 2) if completed > 0 else None

    # Closure code breakdown
    closure_breakdown = (
        week_df.groupby("closure_reason_group")
        .agg(
            tickets=("ticket_id", "count"),
            survey_send_rate=("survey_sent_flag", "mean"),
        )
        .round(3)
        .to_dict("index")
    )

    # Top verbatim themes
    theme_counts = {}
    if "ai_verbatim_theme" in week_df.columns:
        theme_counts = week_df["ai_verbatim_theme"].value_counts().head(5).to_dict()

    # Priority flags
    priority_count = 0
    if "ai_priority_flag" in week_df.columns:
        priority_count = int(week_df["ai_priority_flag"].sum())

    # Agent outliers: agents whose survey send rate is >2 SD below mean
    agent_stats = (
        week_df.groupby("agent_id")
        .agg(tickets=("ticket_id", "count"), send_rate=("survey_sent_flag", "mean"))
        .query("tickets >= 20")
    )
    if len(agent_stats) > 1:
        mean_rate = agent_stats["send_rate"].mean()
        std_rate  = agent_stats["send_rate"].std()
        outliers  = agent_stats[agent_stats["send_rate"] < mean_rate - 2 * std_rate]
        low_send_agents = len(outliers)
    else:
        low_send_agents = 0

    # Week-over-week change
    wow_csat = None
    if len(prev_df) > 0 and completed > 0:
        prev_csat = prev_df["csat_score"].mean()
        if pd.notna(prev_csat):
            wow_csat = round(avg_csat - prev_csat, 2)

    return {
        "week":                   week_str,
        "total_tickets":          total,
        "survey_sent":            sent,
        "survey_send_rate_pct":   safe_rate(sent, total),
        "survey_completed":       completed,
        "response_rate_pct":      safe_rate(completed, sent),
        "avg_csat_score":         avg_csat,
        "wow_csat_change":        wow_csat,
        "closure_code_breakdown": closure_breakdown,
        "top_verbatim_themes":    theme_counts,
        "priority_flag_count":    priority_count,
        "agents_with_low_send_rate": low_send_agents,
    }


def generate_digest(metrics: dict, client: anthropic.Anthropic) -> str:
    """
    Send the weekly metrics to Claude and get a plain-English digest.
    Uses a two-step prompt chain: findings first, then recommendations.
    """

    # Step 1: Generate findings
    findings_prompt = f"""You are a Senior Business Analyst at GM OnStar.
You have been given a structured summary of this week's call center CSAT metrics.
Your job is to write a concise, factual "What We're Seeing" section for a leadership digest.

Rules:
- Be specific and data-grounded. Reference actual numbers from the metrics.
- Do NOT fabricate data not present in the input.
- Highlight the most important 3–4 findings.
- Flag anything that looks like a risk or anomaly.
- Use plain business English. No jargon. No bullet fragments — write complete sentences.
- Length: 150–200 words maximum.

Weekly Metrics:
{json.dumps(metrics, indent=2)}

Write the "What We're Seeing This Week" section now:"""

    findings_response = client.messages.create(
        model=MODEL,
        max_tokens=500,
        messages=[{"role": "user", "content": findings_prompt}]
    )
    findings_text = findings_response.content[0].text.strip()

    # Step 2: Generate recommendations based on findings
    recs_prompt = f"""Based on the findings below, write a "Recommended Actions" section.

Findings:
{findings_text}

Metrics context:
- Survey send rate: {metrics['survey_send_rate_pct']}%
- Response rate: {metrics['response_rate_pct']}%
- Average CSAT: {metrics['avg_csat_score']} / 5
- Agents flagged for low survey send rate: {metrics['agents_with_low_send_rate']}
- Priority escalation comments: {metrics['priority_flag_count']}

Rules:
- Give 2–4 specific, actionable recommendations.
- Each recommendation should name the owner type (Operations, QA, Team Lead, etc.)
- Keep each recommendation to 1–2 sentences.
- Do NOT recommend things not supported by the data.

Write the "Recommended Actions" section now:"""

    recs_response = client.messages.create(
        model=MODEL,
        max_tokens=400,
        messages=[{"role": "user", "content": recs_prompt}]
    )
    recs_text = recs_response.content[0].text.strip()

    # Compose final digest
    digest = f"""
═══════════════════════════════════════════════════════
  GM OnStar CSAT Weekly Digest — {metrics['week']}
  Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}
═══════════════════════════════════════════════════════

HEADLINE METRICS
────────────────
  Total Tickets:     {metrics['total_tickets']:,}
  Surveys Sent:      {metrics['survey_sent']:,}  ({metrics['survey_send_rate_pct']}% send rate)
  Surveys Completed: {metrics['survey_completed']:,}  ({metrics['response_rate_pct']}% response rate)
  Avg CSAT Score:    {metrics['avg_csat_score']} / 5.0{f"  (WoW: {'+' if metrics['wow_csat_change'] > 0 else ''}{metrics['wow_csat_change']})" if metrics['wow_csat_change'] is not None else ''}
  Priority Flags:    {metrics['priority_flag_count']} comments requiring follow-up

WHAT WE'RE SEEING THIS WEEK
────────────────────────────
{findings_text}

RECOMMENDED ACTIONS
────────────────────
{recs_text}

═══════════════════════════════════════════════════════
  For full dashboard: [Power BI Dashboard Link]
  Questions: Chitra (Queen) Dubey | BA Lead
═══════════════════════════════════════════════════════
"""
    return digest.strip()


def main(input_path: str, week_str: str, output_path: str = None):
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        raise EnvironmentError("ANTHROPIC_API_KEY environment variable not set.")

    print(f"📂 Loading {input_path}...")
    df = pd.read_csv(input_path)

    print(f"📊 Computing metrics for {week_str}...")
    metrics = compute_weekly_metrics(df, week_str)

    print("🤖 Generating AI digest...")
    client = anthropic.Anthropic(api_key=api_key)
    digest = generate_digest(metrics, client)

    print("\n" + digest)

    if output_path:
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        with open(output_path, "w") as f:
            f.write(digest)
        print(f"\n✅ Digest saved to {output_path}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--input",  default="data/processed/master_with_themes.csv")
    parser.add_argument("--week",   default=datetime.now().strftime("%G-W%V"),
                        help="ISO week, e.g. 2026-W22")
    parser.add_argument("--output", default=None, help="Optional: save digest to file")
    args = parser.parse_args()
    main(args.input, args.week, args.output)
