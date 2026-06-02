"""
sample_data_generator.py
========================
GM OnStar CSAT Improvement Project
Generates synthetic sample data for testing and portfolio demonstration.

All data is fictional. No real customer or agent data is used.

Usage:
    python data/sample/sample_data_generator.py
    python data/sample/sample_data_generator.py --rows 5000 --months 6

Output:
    data/sample/sample_tickets.csv
    data/sample/sample_surveys.csv
    data/sample/sample_telephony.csv
    data/sample/sample_master.csv
"""

import pandas as pd
import numpy as np
import random
import argparse
from datetime import datetime, timedelta
import os

# ─────────────────────────────────────────────────────────────────────────────
# Configuration
# ─────────────────────────────────────────────────────────────────────────────
SEED = 42
np.random.seed(SEED)
random.seed(SEED)

CLOSURE_CODES = {
    "RES_CONF":         {"group": "Resolved - Customer Confirmed",  "survey_rate": 0.85},
    "RES_CUST_VERIFIED":{"group": "Resolved - Customer Confirmed",  "survey_rate": 0.82},
    "SOLVED_FIRST":     {"group": "Resolved - Customer Confirmed",  "survey_rate": 0.88},
    "RES_NO_FU":        {"group": "Resolved - No Follow-Up",        "survey_rate": 0.22},
    "SOLVED_SILENT":    {"group": "Resolved - No Follow-Up",        "survey_rate": 0.18},
    "CLOSED_AUTO":      {"group": "Resolved - No Follow-Up",        "survey_rate": 0.12},
    "ESCALATED_T2":     {"group": "Escalated",                      "survey_rate": 0.60},
    "ESCALATED_SUP":    {"group": "Escalated",                      "survey_rate": 0.55},
    "TRANSFERRED_DEPT": {"group": "Transferred",                    "survey_rate": 0.45},
    "TRANSFERRED_EXT":  {"group": "Transferred",                    "survey_rate": 0.40},
    "DUPLICATE":        {"group": "Administrative",                 "survey_rate": 0.05},
}

ISSUE_CATEGORIES = [
    "Navigation", "Connectivity", "Emergency Services",
    "Billing", "Remote Services", "Diagnostics"
]

CHANNELS = ["phone", "phone", "phone", "chat", "app"]  # weighted toward phone

AGENTS = [
    {"id": f"AGT{str(i).zfill(3)}", "name": f"Agent_{i:03d}", "team": f"TEAM{(i % 4) + 1}"}
    for i in range(1, 31)
]

# Some agents have behavioral patterns (suppress surveys by using low-trigger codes)
# Agents 25-30 use low-trigger codes more often (simulating the behavior pattern)
AGENT_CODE_BIAS = {
    f"AGT{str(i).zfill(3)}": "low" for i in range(25, 31)
}

CSAT_BY_RESOLUTION = {
    "resolved":   {"mean": 4.1, "std": 0.7},
    "escalated":  {"mean": 3.2, "std": 0.9},
    "transferred":{"mean": 3.5, "std": 0.8},
    "unresolved": {"mean": 2.1, "std": 0.8},
    "abandoned":  {"mean": 2.5, "std": 0.9},
}

VERBATIM_TEMPLATES = {
    "positive": [
        "Agent was very helpful and resolved my issue quickly.",
        "Excellent service, very professional.",
        "Fast resolution, very satisfied.",
        "Agent was knowledgeable and patient.",
    ],
    "neutral": [
        "Issue was resolved but took longer than expected.",
        "Okay experience overall.",
        "Got it sorted out eventually.",
        "Acceptable service.",
    ],
    "negative": [
        "Was transferred multiple times with no resolution.",
        "Long wait time and the agent was unhelpful.",
        "Still not resolved after this call.",
        "Very frustrating experience.",
        "Had to call back multiple times for the same issue.",
    ],
}


def generate_tickets(n_rows: int, start_date: datetime, end_date: datetime) -> pd.DataFrame:
    """Generate synthetic ticket / CRM data."""
    records = []
    date_range = (end_date - start_date).days

    for i in range(n_rows):
        agent = random.choice(AGENTS)
        is_biased = AGENT_CODE_BIAS.get(agent["id"]) == "low"

        # Agents with bias toward low-trigger codes use them ~70% of the time
        code_pool = (
            ["RES_NO_FU", "SOLVED_SILENT", "CLOSED_AUTO", "DUPLICATE"]
            if is_biased and random.random() < 0.70
            else list(CLOSURE_CODES.keys())
        )
        closure_code = random.choice(code_pool)

        opened_at = start_date + timedelta(
            days=random.randint(0, date_range),
            hours=random.randint(7, 21),
            minutes=random.randint(0, 59)
        )
        handle_seconds = max(30, int(np.random.lognormal(mean=6.0, sigma=0.7)))
        closed_at = opened_at + timedelta(seconds=handle_seconds)

        transfer_count = np.random.choice([0, 1, 2, 3], p=[0.70, 0.20, 0.07, 0.03])
        resolution = (
            "transferred" if transfer_count > 0
            else random.choices(
                ["resolved", "escalated", "unresolved", "abandoned"],
                weights=[0.75, 0.12, 0.08, 0.05]
            )[0]
        )

        records.append({
            "ticket_id":           f"TKT{str(i + 1).zfill(7)}",
            "agent_id":            agent["id"],
            "agent_name":          agent["name"],
            "team_id":             agent["team"],
            "ticket_opened_at":    opened_at.isoformat(),
            "ticket_closed_at":    closed_at.isoformat(),
            "handle_time_seconds": handle_seconds,
            "closure_reason_code": closure_code,
            "closure_reason_group": CLOSURE_CODES[closure_code]["group"],
            "channel":             random.choice(CHANNELS),
            "issue_category":      random.choice(ISSUE_CATEGORIES),
            "resolution_status":   resolution,
            "transfer_count":      transfer_count,
            "is_escalation":       resolution == "escalated",
        })

    return pd.DataFrame(records)


def generate_surveys(tickets_df: pd.DataFrame) -> pd.DataFrame:
    """Generate synthetic survey data based on closure code survey rates."""
    survey_records = []

    for _, row in tickets_df.iterrows():
        code = row["closure_reason_code"]
        send_rate = CLOSURE_CODES.get(code, {}).get("survey_rate", 0.50)

        if random.random() > send_rate:
            continue  # No survey sent for this ticket

        sent_at = datetime.fromisoformat(row["ticket_closed_at"]) + timedelta(
            hours=random.choices([2, 24, 48, 96], weights=[0.4, 0.35, 0.15, 0.10])[0]
        )

        # Completion rate influenced by days delay — faster = higher completion
        delay_hours = (sent_at - datetime.fromisoformat(row["ticket_closed_at"])).total_seconds() / 3600
        completion_rate = max(0.10, 0.55 - (delay_hours / 200))
        completed = random.random() < completion_rate

        csat_score = None
        verbatim = None
        completed_at = None

        if completed:
            completed_at = (sent_at + timedelta(hours=random.randint(1, 48))).isoformat()
            resolution = row["resolution_status"]
            params = CSAT_BY_RESOLUTION.get(resolution, {"mean": 3.5, "std": 0.8})
            raw = np.random.normal(params["mean"], params["std"])
            csat_score = round(max(1.0, min(5.0, raw)), 1)

            # Verbatim: ~40% of completions include open text
            if random.random() < 0.40:
                sentiment = (
                    "positive" if csat_score >= 4.0
                    else "negative" if csat_score <= 2.5
                    else "neutral"
                )
                verbatim = random.choice(VERBATIM_TEMPLATES[sentiment])

        survey_records.append({
            "ticket_id":            row["ticket_id"],
            "survey_sent_flag":     1,
            "survey_sent_at":       sent_at.isoformat(),
            "survey_completed_flag": 1 if completed else 0,
            "survey_completed_at":  completed_at,
            "csat_score":           csat_score,
            "verbatim_comment":     verbatim,
            "survey_trigger_method": "closure_code",
        })

    return pd.DataFrame(survey_records)


def build_master(tickets_df: pd.DataFrame, surveys_df: pd.DataFrame) -> pd.DataFrame:
    """Join tickets and surveys into the master analytical dataset."""
    master = tickets_df.merge(surveys_df, on="ticket_id", how="left")
    master["survey_sent_flag"] = master["survey_sent_flag"].fillna(0).astype(int)
    master["survey_completed_flag"] = master["survey_completed_flag"].fillna(0).astype(int)

    # Derived fields
    closed = pd.to_datetime(master["ticket_closed_at"])
    master["day_of_week"] = closed.dt.day_name()
    master["hour_of_day"] = closed.dt.hour
    master["month_year"] = closed.dt.to_period("M").astype(str)

    master["handle_time_bucket"] = pd.cut(
        master["handle_time_seconds"],
        bins=[0, 180, 420, 900, float("inf")],
        labels=["0-3min", "3-7min", "7-15min", "15+min"]
    )

    return master


def main(n_rows: int = 3000, months: int = 6):
    end_date = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
    start_date = end_date - timedelta(days=months * 30)

    print(f"Generating {n_rows} tickets from {start_date.date()} to {end_date.date()}...")

    tickets_df = generate_tickets(n_rows, start_date, end_date)
    surveys_df = generate_surveys(tickets_df)
    master_df = build_master(tickets_df, surveys_df)

    os.makedirs("data/sample", exist_ok=True)
    tickets_df.to_csv("data/sample/sample_tickets.csv", index=False)
    surveys_df.to_csv("data/sample/sample_surveys.csv", index=False)
    master_df.to_csv("data/sample/sample_master.csv", index=False)

    print(f"\n✅ Files written to data/sample/")
    print(f"   Tickets:  {len(tickets_df):,}")
    print(f"   Surveys:  {len(surveys_df):,} ({len(surveys_df)/len(tickets_df)*100:.1f}% send rate)")
    completed = surveys_df["survey_completed_flag"].sum()
    print(f"   Completed:{completed:,} ({completed/len(surveys_df)*100:.1f}% response rate)")
    print(f"   Master:   {len(master_df):,} rows, {len(master_df.columns)} columns")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate synthetic OnStar CSAT data")
    parser.add_argument("--rows", type=int, default=3000, help="Number of ticket rows")
    parser.add_argument("--months", type=int, default=6, help="Months of history")
    args = parser.parse_args()
    main(n_rows=args.rows, months=args.months)
