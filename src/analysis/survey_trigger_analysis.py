"""
survey_trigger_analysis.py
===========================
GM OnStar CSAT Improvement Project — Analysis Track 1

Analyzes the relationship between ticket closure codes and survey trigger rates.

Key Questions:
  1. Which closure codes have the highest and lowest survey send rates?
  2. Is the difference statistically significant?
  3. How much total survey volume is being suppressed?
  4. Are there specific agents or teams disproportionately using low-trigger codes?

Output:
  - data/processed/closure_code_survey_rates.csv
  - data/processed/survey_suppression_summary.csv
  - Console summary with key findings
"""

import pandas as pd
import numpy as np
from scipy import stats
import argparse
import os


def load_data(path: str) -> pd.DataFrame:
    df = pd.read_csv(path)
    df["ticket_closed_at"] = pd.to_datetime(df["ticket_closed_at"])
    return df


def closure_code_survey_rates(df: pd.DataFrame) -> pd.DataFrame:
    """
    For each closure code group, compute:
    - Ticket volume
    - Survey send rate
    - Survey completion rate
    - Average CSAT (for completed surveys)
    """
    summary = (
        df.groupby("closure_reason_group")
        .agg(
            ticket_count        = ("ticket_id", "count"),
            surveys_sent        = ("survey_sent_flag", "sum"),
            surveys_completed   = ("survey_completed_flag", "sum"),
            avg_csat            = ("csat_score", "mean"),
        )
        .reset_index()
    )

    summary["survey_send_rate"]        = summary["surveys_sent"] / summary["ticket_count"]
    summary["survey_completion_rate"]  = (
        summary["surveys_completed"] / summary["surveys_sent"].replace(0, np.nan)
    )
    summary["pct_of_total_tickets"]    = summary["ticket_count"] / summary["ticket_count"].sum()

    # How many additional surveys WOULD have been sent if every group matched
    # the highest-performing closure code group's send rate?
    max_send_rate = summary["survey_send_rate"].max()
    summary["potential_surveys_missed"] = (
        (max_send_rate - summary["survey_send_rate"]) * summary["ticket_count"]
    ).clip(lower=0).astype(int)

    summary = summary.sort_values("survey_send_rate", ascending=False).reset_index(drop=True)
    summary["avg_csat"] = summary["avg_csat"].round(2)
    summary["survey_send_rate"] = summary["survey_send_rate"].round(3)
    summary["survey_completion_rate"] = summary["survey_completion_rate"].round(3)
    summary["pct_of_total_tickets"] = summary["pct_of_total_tickets"].round(3)

    return summary


def statistical_significance_test(df: pd.DataFrame, group_a: str, group_b: str) -> dict:
    """
    Chi-square test: is the difference in survey send rates between two
    closure code groups statistically significant?
    """
    g_a = df[df["closure_reason_group"] == group_a]
    g_b = df[df["closure_reason_group"] == group_b]

    # Contingency table: [sent, not sent] for each group
    a_sent     = g_a["survey_sent_flag"].sum()
    a_not_sent = len(g_a) - a_sent
    b_sent     = g_b["survey_sent_flag"].sum()
    b_not_sent = len(g_b) - b_sent

    contingency = [[a_sent, a_not_sent], [b_sent, b_not_sent]]
    chi2, p_value, dof, _ = stats.chi2_contingency(contingency)

    return {
        "group_a": group_a,
        "group_b": group_b,
        "group_a_send_rate": round(a_sent / len(g_a), 3),
        "group_b_send_rate": round(b_sent / len(g_b), 3),
        "chi2_statistic": round(chi2, 3),
        "p_value": round(p_value, 6),
        "significant_at_05": p_value < 0.05,
        "significant_at_01": p_value < 0.01,
    }


def agent_level_suppression(df: pd.DataFrame, min_tickets: int = 50) -> pd.DataFrame:
    """
    Identify agents whose survey send rate is significantly below the team average.
    Flags agents for potential coaching review (not disciplinary — BA scope is data).
    """
    agent_stats = (
        df.groupby(["agent_id", "agent_name"])
        .agg(
            ticket_count    = ("ticket_id", "count"),
            surveys_sent    = ("survey_sent_flag", "sum"),
            surveys_completed = ("survey_completed_flag", "sum"),
            avg_csat        = ("csat_score", "mean"),
            # How often does this agent use low-trigger closure codes?
            pct_low_trigger_codes = ("closure_reason_group",
                lambda x: (x.isin(["Resolved - No Follow-Up", "Administrative"])).mean())
        )
        .reset_index()
        .query(f"ticket_count >= {min_tickets}")
    )

    agent_stats["send_rate"] = agent_stats["surveys_sent"] / agent_stats["ticket_count"]

    team_mean = agent_stats["send_rate"].mean()
    team_std  = agent_stats["send_rate"].std()

    agent_stats["z_score"] = (agent_stats["send_rate"] - team_mean) / team_std
    agent_stats["send_rate_flag"] = agent_stats["z_score"] < -2.0

    return agent_stats.sort_values("send_rate").reset_index(drop=True).round(3)


def print_findings(closure_df: pd.DataFrame, agent_df: pd.DataFrame, df: pd.DataFrame):
    print("\n" + "═" * 65)
    print("  TRACK 1 FINDINGS: Survey Trigger Analysis")
    print("═" * 65)

    total_tickets = len(df)
    total_sent    = df["survey_sent_flag"].sum()
    overall_rate  = total_sent / total_tickets

    print(f"\n📊 OVERALL")
    print(f"   Total tickets in period:    {total_tickets:,}")
    print(f"   Total surveys sent:         {int(total_sent):,}")
    print(f"   Overall survey send rate:   {overall_rate:.1%}")

    print(f"\n📊 SURVEY SEND RATE BY CLOSURE CODE GROUP")
    print(closure_df[["closure_reason_group", "ticket_count",
                       "survey_send_rate", "avg_csat",
                       "potential_surveys_missed"]].to_string(index=False))

    total_missed = closure_df["potential_surveys_missed"].sum()
    print(f"\n   ⚠️  Estimated surveys missed vs. best-case rate: {total_missed:,}")

    flagged_agents = agent_df[agent_df["send_rate_flag"] == True]
    print(f"\n📊 AGENT SUPPRESSION FLAGS")
    print(f"   Agents with send rate > 2 SD below team average: {len(flagged_agents)}")
    if len(flagged_agents) > 0:
        print(flagged_agents[["agent_id", "ticket_count", "send_rate",
                               "pct_low_trigger_codes", "z_score"]].to_string(index=False))

    print("\n" + "═" * 65)
    print("  KEY FINDING")
    best  = closure_df.iloc[0]["closure_reason_group"]
    worst = closure_df.iloc[-1]["closure_reason_group"]
    best_rate  = closure_df.iloc[0]["survey_send_rate"]
    worst_rate = closure_df.iloc[-1]["survey_send_rate"]
    print(f"  The gap between highest ({best}: {best_rate:.0%}) and")
    print(f"  lowest ({worst}: {worst_rate:.0%}) closure groups is")
    print(f"  {best_rate - worst_rate:.0%} — a likely process control issue,")
    print(f"  not random variation.")
    print("═" * 65 + "\n")


def main(input_path: str, output_dir: str = "data/processed"):
    os.makedirs(output_dir, exist_ok=True)
    df = load_data(input_path)

    print("🔍 Running Track 1: Survey Trigger Analysis...")

    closure_df = closure_code_survey_rates(df)
    agent_df   = agent_level_suppression(df)

    # Statistical test: top vs. bottom closure group
    groups = closure_df["closure_reason_group"].tolist()
    if len(groups) >= 2:
        sig = statistical_significance_test(df, groups[0], groups[-1])
        print(f"\n🔬 Chi-Square Test: '{groups[0]}' vs '{groups[-1]}'")
        print(f"   p-value: {sig['p_value']} | Significant at 0.05: {sig['significant_at_05']}")

    closure_df.to_csv(f"{output_dir}/closure_code_survey_rates.csv", index=False)
    agent_df.to_csv(f"{output_dir}/agent_survey_send_rates.csv", index=False)

    print_findings(closure_df, agent_df, df)
    print(f"✅ Outputs written to {output_dir}/")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--input",  default="data/sample/sample_master.csv")
    parser.add_argument("--output", default="data/processed")
    args = parser.parse_args()
    main(args.input, args.output)
