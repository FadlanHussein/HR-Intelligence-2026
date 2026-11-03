
import pandas as pd
import hashlib
import json
from collections import Counter
from decimal import Decimal
from pathlib import Path
from sqlalchemy import create_engine, text

# ==================================================
# 1. CONFIGURATION
# ==================================================

BASE_DIR = Path(__file__).resolve().parent.parent

CSV_PATH = BASE_DIR / "data" / "processed" / "recruitment_candidates_clean.csv"
OUTPUT_DIR = BASE_DIR / "data" / "processed"

DATABASE_URL = "postgresql+psycopg2://postgres:YOUR_PASSWORD@localhost:5432/recruitment_intelligence"

COLUMNS = [
    "age",
    "gender",
    "education_level",
    "experience_years",
    "previous_companies",
    "distance_from_company",
    "interview_score",
    "skill_score",
    "personality_score",
    "recruitment_strategy",
    "hiring_decision"
]

NUMERIC_COLUMNS = [
    "age",
    "experience_years",
    "previous_companies",
    "distance_from_company",
    "interview_score",
    "skill_score",
    "personality_score",
    "hiring_decision"
]

# ==================================================
# 2. NORMALIZE RECORD
# ==================================================

def normalize_value(column, value):

    if pd.isna(value):
        return None

    if column in NUMERIC_COLUMNS:
        number = Decimal(str(value)).normalize()
        return format(number, "f")

    return " ".join(str(value).strip().casefold().split())


def generate_fingerprint(row):

    normalized_record = [
        normalize_value(column, row[column])
        for column in COLUMNS
    ]

    record_string = json.dumps(
        normalized_record,
        ensure_ascii=False
    )

    return hashlib.sha256(
        record_string.encode("utf-8")
    ).hexdigest()


# ==================================================
# 3. READ CSV DATA
# ==================================================

print("\n=== RECORD-LEVEL RECONCILIATION ===")

csv_df = pd.read_csv(CSV_PATH)

missing_columns = [
    column for column in COLUMNS
    if column not in csv_df.columns
]

if missing_columns:
    raise ValueError(
        f"Missing CSV columns: {missing_columns}"
    )

csv_df = csv_df[COLUMNS].copy()

print(f"CSV records: {len(csv_df)}")


# ==================================================
# 4. READ DATABASE DATA
# ==================================================

engine = create_engine(DATABASE_URL)

query = text("""
    SELECT
        age,
        gender,
        education_level,
        experience_years,
        previous_companies,
        distance_from_company,
        interview_score,
        skill_score,
        personality_score,
        recruitment_strategy,
        hiring_decision
    FROM recruitment_candidates
""")

with engine.connect() as connection:
    db_df = pd.read_sql(query, connection)

print(f"Database records: {len(db_df)}")


# ==================================================
# 5. GENERATE RECORD FINGERPRINTS
# ==================================================

csv_fingerprints = [
    generate_fingerprint(row)
    for _, row in csv_df.iterrows()
]

db_fingerprints = [
    generate_fingerprint(row)
    for _, row in db_df.iterrows()
]

csv_counts = Counter(csv_fingerprints)
db_counts = Counter(db_fingerprints)


# ==================================================
# 6. COMPARE RECORDS
# ==================================================

all_fingerprints = sorted(
    set(csv_counts) | set(db_counts)
)

report = []

for fingerprint in all_fingerprints:

    csv_count = csv_counts[fingerprint]
    db_count = db_counts[fingerprint]

    matched_count = min(csv_count, db_count)
    csv_only_count = max(csv_count - db_count, 0)
    db_only_count = max(db_count - csv_count, 0)

    if csv_count == db_count:
        status = "MATCH"

    elif csv_count > db_count:
        status = "CSV_ONLY" if db_count == 0 else "COUNT_MISMATCH"

    else:
        status = (
            "DATABASE_ONLY"
            if csv_count == 0
            else "COUNT_MISMATCH"
        )

    report.append({
        "record_fingerprint": fingerprint,
        "csv_count": csv_count,
        "database_count": db_count,
        "matched_count": matched_count,
        "csv_only_count": csv_only_count,
        "database_only_count": db_only_count,
        "status": status
    })


# ==================================================
# 7. CREATE SUMMARY
# ==================================================

report_df = pd.DataFrame(report)

summary = {
    "csv_records": len(csv_df),
    "database_records": len(db_df),
    "matched_records": int(report_df["matched_count"].sum()),
    "csv_only_records": int(report_df["csv_only_count"].sum()),
    "database_only_records": int(report_df["database_only_count"].sum()),
    "distinct_fingerprints": len(all_fingerprints),
    "matching_fingerprints": int(
        (report_df["status"] == "MATCH").sum()
    ),
    "count_mismatch_fingerprints": int(
        (report_df["status"] == "COUNT_MISMATCH").sum()
    )
}

summary_df = pd.DataFrame(
    list(summary.items()),
    columns=["metric", "value"]
)


# ==================================================
# 8. EXPORT REPORTS
# ==================================================

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

report_path = OUTPUT_DIR / "record_level_reconciliation_report.csv"
summary_path = OUTPUT_DIR / "record_level_reconciliation_summary.csv"

report_df.to_csv(report_path, index=False)
summary_df.to_csv(summary_path, index=False)


# ==================================================
# 9. DISPLAY RESULTS
# ==================================================

print("\n=== RECONCILIATION SUMMARY ===")

for metric, value in summary.items():
    print(f"{metric}: {value}")

print("\n=== RECONCILIATION STATUS ===")

if (
    summary["csv_only_records"] == 0
    and summary["database_only_records"] == 0
):
    print("RESULT: MATCH")
else:
    print("RESULT: MISMATCH")

print("\nReports generated:")
print(report_path)
print(summary_path)

engine.dispose()

