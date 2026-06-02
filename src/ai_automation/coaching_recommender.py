"""
coaching_recommender.py
=======================
GM OnStar CSAT Improvement Project — AI Automation Module

Generates personalized, data-grounded coaching notes for agents
whose patterns warrant review. Output goes to the team lead,
NOT directly to the agent.

This module does NOT make disciplinary recommendations.
It provides factual pattern summaries and development suggestions only.

Usage:
    python src/ai_automation/coaching_recommender.py \
        --input data/processed/agent_survey_send_rates.csv \
        --master data/processed/master_with_themes.csv \
        --output data/processed/coaching_notes.json
"""

import os
import json
import argparse
import pandas as pd
import anthropic
from datetime import datetime


MODEL = "claude-sonnet-4-20250514"


COACHING_PROMPT = """You are a call center quality coach at GM OnStar.
You have been given a data profile for a single agent.
Your job is to write a coaching note for their team lead.

Rules:
- Be specific and factual — reference the exact numbers provided.
- Frame everything as development opportunity, NOT disciplinary language.
- Do NOT use language like "violation", "misconduct", "gaming", or "suspicious."
- Suggest 2–3 specific, actionable coaching behaviors.
- Keep the tone supportive and professional.
- Length: 150–200 words.
- Do NOT fabricate metrics not in the profile.

Agent Profile:
{profile_json}

Write the coaching note now:"""


def build_agent_profile(agent_row: pd.Series, master_df: pd.DataFrame) -> dict:
    """Build a structured profile dict for one agent."""
    agent_df = master_df[master_df["agent_id"] == agent_row["agent_id"]]

    top_closure_codes = (
        agent_df["closure_reason_group"].value_counts(normalize=True)
        .head(3)
        .round(3)
        .to_dict()
    )

    top_themes = {}
    if "ai_verbatim_theme" in agent_df.columns:
        top_themes = (
            agent_df["ai_verbatim_theme"].dropna()
            .value_counts()
            .head(3)
            .to_dict()
        )

    return {
        "agent_id":                   agent_row["agent_id"],
        "total_tickets":              int(agent_row["ticket_count"]),
        "survey_send_rate":           f"{agent_row['send_rate']:.1%}",
        "team_avg_send_rate":         "See context",
        "z_score_vs_team":            round(float(agent_row["z_score"]), 2),
        "pct_low_trigger_codes":      f"{agent_row['pct_low_trigger_codes']:.1%}",
        "avg_csat_score":             round(float(agent_row["avg_csat"]), 2),
        "top_closure_code_groups":    top_closure_codes,
        "top_verbatim_themes":        top_themes,
        "qa_score":                   round(float(agent_row.get("qa_score", 0)), 1)
                                      if pd.notna(agent_row.get("qa_score")) else "Not evaluated",
    }


def generate_coaching_note(profile: dict, client: anthropic.Anthropic) -> str:
    prompt = COACHING_PROMPT.replace(
        "{profile_json}",
        json.dumps(profile, indent=2)
    )
    response = client.messages.create(
        model=MODEL,
        max_tokens=400,
        messages=[{"role": "user", "content": prompt}]
    )
    return response.content[0].text.strip()


def main(agent_path: str, master_path: str, output_path: str):
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        raise EnvironmentError("ANTHROPIC_API_KEY environment variable not set.")

    print("📂 Loading data...")
    agent_df  = pd.read_csv(agent_path)
    master_df = pd.read_csv(master_path)

    # Only generate notes for flagged agents
    flagged = agent_df[agent_df["send_rate_flag"] == True].copy()
    print(f"   {len(flagged)} agents flagged for coaching review")

    if len(flagged) == 0:
        print("   No agents require coaching notes this cycle.")
        return

    client = anthropic.Anthropic(api_key=api_key)
    results = []

    for _, row in flagged.iterrows():
        print(f"   Generating note for {row['agent_id']}...")
        profile = build_agent_profile(row, master_df)
        note    = generate_coaching_note(profile, client)

        results.append({
            "generated_at": datetime.now().isoformat(),
            "agent_id":     row["agent_id"],
            "agent_name":   row.get("agent_name", ""),
            "profile":      profile,
            "coaching_note": note,
            "for_team_lead": True,
            "disclaimer":   "This note is generated from statistical patterns. "
                            "It is a development tool, not a disciplinary record."
        })

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "w") as f:
        json.dump(results, f, indent=2)

    print(f"\n✅ {len(results)} coaching notes written to {output_path}")

    # Print a sample
    if results:
        print(f"\n── Sample Coaching Note ({results[0]['agent_id']}) ──")
        print(results[0]["coaching_note"])


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--input",  default="data/processed/agent_survey_send_rates.csv")
    parser.add_argument("--master", default="data/processed/master_with_themes.csv")
    parser.add_argument("--output", default="data/processed/coaching_notes.json")
    args = parser.parse_args()
    main(args.input, args.master, args.output)
