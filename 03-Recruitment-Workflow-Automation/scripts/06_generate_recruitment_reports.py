import pandas as pd
from pathlib import Path
from datetime import datetime

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data" / "processed"

SUMMARY_FILE = DATA_DIR / "recruitment_summary.csv"
STRATEGY_FILE = DATA_DIR / "recruitment_strategy_summary.csv"
STATUS_FILE = DATA_DIR / "candidate_status_report.csv"

OUTPUT_FILE = DATA_DIR / "recruitment_executive_summary.txt"

print("\n=== AUTOMATED RECRUITMENT SUMMARY ===")

# 1. Load source data
summary_df = pd.read_csv(SUMMARY_FILE)
strategy_df = pd.read_csv(STRATEGY_FILE)
status_df = pd.read_csv(STATUS_FILE)

# 2. Calculate recruitment KPIs
total_candidates = len(status_df)

hired_candidates = (
    status_df["candidate_status"] == "Hired"
).sum()

rejected_candidates = (
    status_df["candidate_status"] == "Rejected"
).sum()

hiring_rate = (
    hired_candidates / total_candidates * 100
    if total_candidates > 0 else 0
)
rejection_rate = (
    rejected_candidates / total_candidates * 100
    if total_candidates > 0 else 0
)

strategy_df["hiring_contribution"] = (
    strategy_df["hired_candidates"] / hired_candidates * 100
    if hired_candidates > 0 else 0
)

strategy_df["rejection_contribution"] = (
    strategy_df["rejected_candidates"] / rejected_candidates * 100
    if rejected_candidates > 0 else 0
)
# 3. Identify highest hiring-rate strategy
best_strategy = strategy_df.loc[
    strategy_df["hiring_rate"].idxmax()
]

# 4. Data reconciliation
summary_values = dict(
    zip(summary_df["metric"], summary_df["value"])
)

checks = {
    "Total Candidates": (
        total_candidates == summary_values["Total Candidates"]
    ),
    "Hired Candidates": (
        hired_candidates == summary_values["Hired Candidates"]
    ),
    "Rejected Candidates": (
        rejected_candidates == summary_values["Rejected Candidates"]
    ),
    "Strategy Candidate Count": (
        strategy_df["total_candidates"].sum() == total_candidates
    )
}

all_checks_passed = all(checks.values())

# 5. Generate report content
report = []

report.append("RECRUITMENT EXECUTIVE SUMMARY")
report.append("=" * 35)
report.append(f"Generated At: {datetime.now():%Y-%m-%d %H:%M:%S}")
report.append("")

report.append("RECRUITMENT OVERVIEW")
report.append(f"Total Candidates : {total_candidates:,}")
report.append(f"Hired Candidates : {hired_candidates:,}")
report.append(f"Rejected Candidates : {rejected_candidates:,}")
report.append(f"Hiring Rate : {hiring_rate:.2f}%")
report.append(f"Rejection Rate : {rejection_rate:.2f}%")
report.append("")

report.append("RECRUITMENT STRATEGY PERFORMANCE")

for _, row in strategy_df.iterrows():
    report.append(
        f"{row['recruitment_strategy']}: "
        f"{row['hired_candidates']:,} hired / "
        f"{row['total_candidates']:,} candidates "
        f"({row['hiring_rate']:.2f}% hiring rate)"
    )

    report.append(
        f"  Hiring Contribution: "
        f"{row['hiring_contribution']:.2f}%"
    )

    report.append(
        f"  Rejection Contribution: "
        f"{row['rejection_contribution']:.2f}%"
    )

report.append("")
report.append("DATA RECONCILIATION")

for check_name, result in checks.items():
    status = "PASS" if result else "FAIL"
    report.append(f"{check_name}: {status}")

report.append("")
report.append(
    "Overall Reporting Status: "
    + ("APPROVED" if all_checks_passed else "REVIEW REQUIRED")
)

report.append("")
report.append(
    "Note: Strategy comparisons are descriptive and do not "
    "establish causal effectiveness."
)

# 6. Save report
with open(OUTPUT_FILE, "w", encoding="utf-8") as file:
    file.write("\n".join(report))

print("\n".join(report))

print(f"\nReport saved to: {OUTPUT_FILE}")
