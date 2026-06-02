"""
verbatim_classifier.py
======================
GM OnStar CSAT Improvement Project — AI Automation Module

Uses the Anthropic Claude API to classify open-text survey verbatims into:
  - Theme category (resolution_quality, wait_time, agent_attitude, etc.)
  - Sentiment (positive, neutral, negative)
  - Priority flag (whether it warrants immediate escalation)

This replaces manual tagging and enables consistent, scalable analysis
of thousands of verbatim comments.

Requirements:
    pip install anthropic pandas tqdm

Environment Variables:
    ANTHROPIC_API_KEY — your Anthropic API key

Usage:
    python src/ai_automation/verbatim_classifier.py \
        --input data/sample/sample_master.csv \
        --output data/processed/master_with_themes.csv \
        --batch-size 20
"""

import os
import json
import time
import argparse
import pandas as pd
from tqdm import tqdm
import anthropic

# ─────────────────────────────────────────────────────────────────────────────
# Configuration
# ─────────────────────────────────────────────────────────────────────────────
MODEL = "claude-sonnet-4-20250514"
MAX_TOKENS = 1024
RATE_LIMIT_PAUSE = 1.0  # seconds between batches

THEMES = [
    "resolution_quality",
    "wait_time",
    "agent_attitude",
    "technical_issue",
    "billing",
    "navigation",
    "transfer_experience",
    "other",
]

CLASSIFICATION_PROMPT = """You are a customer experience analyst at GM OnStar.
Your task is to classify customer survey verbatim comments.

For each comment, return a JSON object with exactly these fields:
- "theme": one of {themes}
- "sentiment": one of ["positive", "neutral", "negative"]
- "priority_flag": true if the comment indicates an urgent unresolved issue, safety concern, or extreme dissatisfaction — false otherwise
- "confidence": a float from 0.0 to 1.0 indicating your confidence

Return ONLY a JSON array, one object per comment, in the same order as input.
No preamble, no markdown, no explanation.

Comments to classify:
{comments_json}
""".format(themes=THEMES, comments_json="{comments_json}")


def build_batch_prompt(comments: list[str]) -> str:
    """Format a batch of comments into the classification prompt."""
    return CLASSIFICATION_PROMPT.replace(
        "{comments_json}",
        json.dumps([{"index": i, "text": c} for i, c in enumerate(comments)], indent=2)
    )


def classify_batch(client: anthropic.Anthropic, comments: list[str]) -> list[dict]:
    """Send a batch of verbatims to Claude for classification."""
    if not comments:
        return []

    prompt = build_batch_prompt(comments)

    try:
        message = client.messages.create(
            model=MODEL,
            max_tokens=MAX_TOKENS,
            messages=[{"role": "user", "content": prompt}]
        )
        raw = message.content[0].text.strip()

        # Strip markdown fences if present
        if raw.startswith("```"):
            raw = raw.split("```")[1]
            if raw.startswith("json"):
                raw = raw[4:]

        results = json.loads(raw)
        return results

    except json.JSONDecodeError as e:
        print(f"  ⚠️  JSON parse error on batch: {e}")
        return [{"theme": "other", "sentiment": "neutral",
                 "priority_flag": False, "confidence": 0.0}] * len(comments)
    except anthropic.RateLimitError:
        print("  ⚠️  Rate limit hit — waiting 60 seconds...")
        time.sleep(60)
        return classify_batch(client, comments)  # retry
    except Exception as e:
        print(f"  ⚠️  API error: {e}")
        return [{"theme": "other", "sentiment": "neutral",
                 "priority_flag": False, "confidence": 0.0}] * len(comments)


def run_classification(
    input_path: str,
    output_path: str,
    batch_size: int = 20,
    verbatim_col: str = "verbatim_comment",
    dry_run: bool = False
) -> pd.DataFrame:
    """
    Main pipeline: load data, classify verbatims, append results, save.
    """
    print(f"\n📂 Loading data from {input_path}...")
    df = pd.read_csv(input_path)

    # Filter to rows with non-null verbatims
    verbatim_mask = df[verbatim_col].notna() & (df[verbatim_col].str.strip() != "")
    verbatim_df = df[verbatim_mask].copy()
    print(f"   {len(verbatim_df):,} rows with verbatim text out of {len(df):,} total")

    if len(verbatim_df) == 0:
        print("   No verbatims to classify.")
        return df

    # Initialize result columns
    df["ai_verbatim_theme"]     = None
    df["ai_verbatim_sentiment"] = None
    df["ai_priority_flag"]      = None
    df["ai_confidence"]         = None

    if dry_run:
        print("   [DRY RUN] Skipping API calls — writing mock classifications.")
        df.loc[verbatim_mask, "ai_verbatim_theme"]     = "resolution_quality"
        df.loc[verbatim_mask, "ai_verbatim_sentiment"] = "neutral"
        df.loc[verbatim_mask, "ai_priority_flag"]      = False
        df.loc[verbatim_mask, "ai_confidence"]         = 0.99
        df.to_csv(output_path, index=False)
        print(f"✅ Dry run complete → {output_path}")
        return df

    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        raise EnvironmentError("ANTHROPIC_API_KEY environment variable not set.")

    client = anthropic.Anthropic(api_key=api_key)
    indices = verbatim_df.index.tolist()
    comments = verbatim_df[verbatim_col].tolist()

    print(f"\n🤖 Classifying {len(comments):,} verbatims in batches of {batch_size}...")
    all_results = []

    for batch_start in tqdm(range(0, len(comments), batch_size)):
        batch_comments = comments[batch_start: batch_start + batch_size]
        batch_results = classify_batch(client, batch_comments)
        all_results.extend(batch_results)
        time.sleep(RATE_LIMIT_PAUSE)

    # Write results back to dataframe
    for i, (orig_idx, result) in enumerate(zip(indices, all_results)):
        df.at[orig_idx, "ai_verbatim_theme"]     = result.get("theme", "other")
        df.at[orig_idx, "ai_verbatim_sentiment"] = result.get("sentiment", "neutral")
        df.at[orig_idx, "ai_priority_flag"]       = result.get("priority_flag", False)
        df.at[orig_idx, "ai_confidence"]          = result.get("confidence", 0.0)

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    df.to_csv(output_path, index=False)

    # Print summary
    classified = df[verbatim_mask]
    print(f"\n✅ Classification complete → {output_path}")
    print("\n📊 Theme Distribution:")
    print(classified["ai_verbatim_theme"].value_counts().to_string())
    print("\n📊 Sentiment Distribution:")
    print(classified["ai_verbatim_sentiment"].value_counts().to_string())
    print(f"\n🚨 Priority Flags: {classified['ai_priority_flag'].sum()} escalation-worthy comments")

    return df


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="AI verbatim classifier for OnStar CSAT data")
    parser.add_argument("--input",      default="data/sample/sample_master.csv")
    parser.add_argument("--output",     default="data/processed/master_with_themes.csv")
    parser.add_argument("--batch-size", type=int, default=20)
    parser.add_argument("--dry-run",    action="store_true",
                        help="Run without API calls (uses mock classifications)")
    args = parser.parse_args()

    run_classification(
        input_path=args.input,
        output_path=args.output,
        batch_size=args.batch_size,
        dry_run=args.dry_run
    )
