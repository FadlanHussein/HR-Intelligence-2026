from pathlib import Path
import pandas as pd

# 1. Define project directory
BASE_DIR = Path(__file__).resolve().parent.parent

# 2. Define input path
INPUT_PATH = (
    BASE_DIR
    / "data"
    / "processed"
    / "recruitment_candidates_clean.csv"
)

# 3. Read candidate dataset
df = pd.read_csv(INPUT_PATH)

# 4. Display dataset information
print("\n=== RECRUITMENT WORKFLOW AUTOMATION ===")

print(f"Total candidates : {len(df)}")
print(f"Total columns    : {len(df.columns)}")

print("\nCANDIDATE DATA SAMPLE")
print(df.head())

print("\nHIRING DECISION DISTRIBUTION")
print(df["hiring_decision"].value_counts())

# 5. Map hiring decision to candidate status

STATUS_MAPPING = {
    1: "Hired",
    0: "Rejected"
}

df["candidate_status"] = (
    df["hiring_decision"]
    .map(STATUS_MAPPING)
)

print("\n=== CANDIDATE STATUS DISTRIBUTION ===")
print(df["candidate_status"].value_counts())

print("\n=== CANDIDATE STATUS SAMPLE ===")
print(
    df[
        ["hiring_decision", "candidate_status"]
    ].head(10)
)

# 6. Generate recruitment summary

total_candidates = len(df)
total_hired = (df["candidate_status"] == "Hired").sum()
total_rejected = (df["candidate_status"] == "Rejected").sum()

hiring_rate = (
    total_hired / total_candidates * 100
    if total_candidates > 0
    else 0
)

recruitment_summary = pd.DataFrame({
    "metric": [
        "Total Candidates",
        "Hired Candidates",
        "Rejected Candidates",
        "Hiring Rate (%)"
    ],
    "value": [
        total_candidates,
        total_hired,
        total_rejected,
        round(hiring_rate, 2)
    ]
})

print("\n=== RECRUITMENT SUMMARY ===")
print(recruitment_summary.to_string(index=False))

# 7. Analyze recruitment strategy

strategy_summary = (
    df.groupby("recruitment_strategy")
    .agg(
        total_candidates=("candidate_status", "count"),
        hired_candidates=(
            "candidate_status",
            lambda x: (x == "Hired").sum()
        ),
        rejected_candidates=(
            "candidate_status",
            lambda x: (x == "Rejected").sum()
        )
    )
    .reset_index()
)

strategy_summary["hiring_rate"] = (
    strategy_summary["hired_candidates"]
    / strategy_summary["total_candidates"]
    * 100
).round(2)

print("\n=== RECRUITMENT STRATEGY SUMMARY ===")
print(strategy_summary.to_string(index=False))

# 8. Export workflow reports

OUTPUT_DIR = BASE_DIR / "data" / "processed"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# Export candidate status
candidate_status_path = (
    OUTPUT_DIR / "candidate_status_report.csv"
)

df.to_csv(candidate_status_path, index=False)

# Export recruitment summary
recruitment_summary_path = (
    OUTPUT_DIR / "recruitment_summary.csv"
)

recruitment_summary.to_csv(
    recruitment_summary_path,
    index=False
)

# Export strategy summary
strategy_summary_path = (
    OUTPUT_DIR / "recruitment_strategy_summary.csv"
)

strategy_summary.to_csv(
    strategy_summary_path,
    index=False
)

print("\n=== WORKFLOW REPORT EXPORT ===")
print("Candidate status report : SAVED")
print("Recruitment summary     : SAVED")
print("Strategy summary        : SAVED")

print("\n=== OUTPUT FILES ===")
print(candidate_status_path)
print(recruitment_summary_path)
print(strategy_summary_path)

# 9. Recruitment performance monitoring

overall_hiring_rate = hiring_rate

strategy_summary["performance_status"] = (
    strategy_summary["hiring_rate"]
    .apply(
        lambda rate:
        "BELOW BENCHMARK"
        if rate < overall_hiring_rate
        else "AT OR ABOVE BENCHMARK"
    )
)

print("\n=== RECRUITMENT PERFORMANCE MONITORING ===")
print(f"Overall hiring rate : {overall_hiring_rate:.2f}%")
print(f"Benchmark           : {overall_hiring_rate:.2f}%")

print("\n=== STRATEGY PERFORMANCE STATUS ===")
print(
    strategy_summary[
        [
            "recruitment_strategy",
            "hiring_rate",
            "performance_status"
        ]
    ].to_string(index=False)
)

# 10. Generate recruitment exception report

exception_report = strategy_summary[
    strategy_summary["performance_status"] == "BELOW BENCHMARK"
].copy()

print("\n=== RECRUITMENT EXCEPTION REPORT ===")

if exception_report.empty:
    print("No recruitment exceptions detected.")
else:
    print(exception_report.to_string(index=False))

# Export exception report
exception_path = (
    OUTPUT_DIR / "recruitment_exception_report.csv"
)

exception_report.to_csv(exception_path, index=False)

print("\n=== EXCEPTION REPORT EXPORT ===")
print("Exception report : SAVED")
print(f"Output path      : {exception_path}")
print(f"Exception count  : {len(exception_report)}")

# 11. Monitoring quality control

print("\n=== MONITORING QUALITY CONTROL ===")

# Check 1: Candidate count reconciliation
strategy_candidate_total = strategy_summary[
    "total_candidates"
].sum()

check_candidate_count = (
    strategy_candidate_total == total_candidates
)

# Check 2: Hiring decision reconciliation
decision_total = total_hired + total_rejected

check_decision_total = (
    decision_total == total_candidates
)

# Check 3: Exception report validation
check_exception_status = (
    exception_report["performance_status"]
    .eq("BELOW BENCHMARK")
    .all()
)

print(
    f"Candidate count reconciliation : "
    f"{'PASS' if check_candidate_count else 'FAIL'}"
)

print(
    f"Hiring decision reconciliation : "
    f"{'PASS' if check_decision_total else 'FAIL'}"
)

print(
    f"Exception status validation    : "
    f"{'PASS' if check_exception_status else 'FAIL'}"
)

# Overall monitoring status
monitoring_checks = [
    check_candidate_count,
    check_decision_total,
    check_exception_status
]

monitoring_status = (
    "APPROVED"
    if all(monitoring_checks)
    else "REJECTED"
)

print(f"\nOverall monitoring status      : {monitoring_status}")