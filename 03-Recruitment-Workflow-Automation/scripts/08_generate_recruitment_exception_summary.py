import pandas as pd
from pathlib import Path
from datetime import datetime

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data" / "processed"

STRATEGY_FILE = DATA_DIR / "recruitment_strategy_summary.csv"
STATUS_FILE = DATA_DIR / "candidate_status_report.csv"

OUTPUT_FILE = DATA_DIR / "automated_exception_summary.csv"
TEXT_REPORT = DATA_DIR / "automated_exception_summary.txt"

print("\n=== AUTOMATED EXCEPTION SUMMARY ===")

# 1. Load data
strategy_df = pd.read_csv(STRATEGY_FILE)
candidate_df = pd.read_csv(STATUS_FILE)

# 2. Calculate benchmark
total_candidates = len(candidate_df)
hired_candidates = (
    candidate_df["candidate_status"] == "Hired"
).sum()

benchmark = (
    hired_candidates / total_candidates * 100
    if total_candidates > 0 else 0
)

# 3. Detect exceptions
strategy_df["benchmark"] = benchmark

strategy_df["variance"] = (
    strategy_df["hiring_rate"] - benchmark
).round(2)

strategy_df["exception_status"] = strategy_df[
    "hiring_rate"
].apply(
    lambda rate: (
        "BELOW BENCHMARK"
        if rate < benchmark
        else "ABOVE BENCHMARK"
    )
)

exception_df = strategy_df[
    strategy_df["exception_status"] == "BELOW BENCHMARK"
].copy()

# 4. Save CSV
exception_df.to_csv(OUTPUT_FILE, index=False)

# 5. Generate text report
lines = [
    "AUTOMATED RECRUITMENT EXCEPTION SUMMARY",
    "=" * 45,
    f"Generated At: {datetime.now():%Y-%m-%d %H:%M:%S}",
    f"Overall Hiring Rate Benchmark: {benchmark:.2f}%",
    "",
    "STRATEGIES BELOW BENCHMARK"
]

if exception_df.empty:
    lines.append("No below-benchmark strategy detected.")
else:
    for _, row in exception_df.iterrows():
        lines.append(
            f"{row['recruitment_strategy']}: "
            f"{row['hiring_rate']:.2f}% "
            f"(Variance: {row['variance']:.2f} percentage points)"
        )

lines.extend([
    "",
    f"Total Exceptions: {len(exception_df)}",
    "",
    "NOTE: This is a descriptive comparison, not a causal",
    "assessment of recruitment strategy effectiveness."
])

with open(TEXT_REPORT, "w", encoding="utf-8") as file:
    file.write("\n".join(lines))

# 6. Display result
print("\n".join(lines))
print(f"\nCSV saved: {OUTPUT_FILE}")
print(f"Text report saved: {TEXT_REPORT}")
print("\nException reporting: COMPLETED")