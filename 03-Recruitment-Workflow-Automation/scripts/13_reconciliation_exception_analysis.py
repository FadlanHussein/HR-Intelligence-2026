
import pandas as pd
import hashlib
import json
from collections import Counter
from decimal import Decimal
from pathlib import Path
from sqlalchemy import create_engine, text

# Configuration
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


# Normalize record values
def normalize_value(column, value):
    if pd.isna(value):
        return None

    if column in NUMERIC_COLUMNS:
        number = Decimal(str(value)).normalize()
        return format(number, "f")

    return " ".join(str(value).strip().casefold().split())


# Generate record fingerprint
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


# Read CSV data
print("\n=== RECONCILIATION EXCEPTION ANALYSIS ===")

csv_df = pd.read_csv(CSV_PATH)

missing_columns = [
    column for column in COLUMNS
    if column not in csv_df.columns
]

if missing_columns:
    raise ValueError(f"Missing CSV columns: {missing_columns}")

csv_df = csv_df[COLUMNS].copy()

csv_fingerprints = [
    generate_fingerprint(row)
    for _, row in csv_df.iterrows()
]

csv_counts = Counter(csv_fingerprints)


# Read database data
engine = create_engine(DATABASE_URL)

query = text("""
    SELECT
        candidate_id,
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
        hiring_decision,
        score_band,
        score_band_order
    FROM recruitment_candidates
    ORDER BY candidate_id
""")

with engine.connect() as connection:
    db_df = pd.read_sql(query, connection)


# Identify database-only records
remaining_csv_counts = csv_counts.copy()

exceptions = []

for _, row in db_df.iterrows():
    fingerprint = generate_fingerprint(row)

    if remaining_csv_counts[fingerprint] > 0:
        remaining_csv_counts[fingerprint] -= 1
    else:
        exception = row.to_dict()
        exception["record_fingerprint"] = fingerprint
        exception["exception_type"] = "DATABASE_ONLY"
        exception["review_status"] = "PENDING_REVIEW"

        exceptions.append(exception)


# Generate exception report
exception_df = pd.DataFrame(exceptions)

if exception_df.empty:
    print("\nNo database-only records found.")
else:
    exception_df.to_csv(
        OUTPUT_DIR / "reconciliation_exception_details.csv",
        index=False
    )


# Generate exception summary
summary = {
    "database_records": len(db_df),
    "csv_records": len(csv_df),
    "database_only_records": len(exception_df),
    "exception_type": "DATABASE_ONLY",
    "review_status": "PENDING_REVIEW"
}

summary_df = pd.DataFrame(
    list(summary.items()),
    columns=["metric", "value"]
)

summary_df.to_csv(
    OUTPUT_DIR / "reconciliation_exception_summary.csv",
    index=False
)


# Display results
print("\n=== EXCEPTION SUMMARY ===")

for metric, value in summary.items():
    print(f"{metric}: {value}")

if not exception_df.empty:
    print("\n=== EXCEPTION CANDIDATE DETAILS ===")

    print(
        exception_df[
            ["candidate_id", "age", "gender", "education_level",
             "recruitment_strategy", "hiring_decision",
             "score_band", "review_status"]
        ].to_string(index=False)
    )

print("\nReports generated:")
print(OUTPUT_DIR / "reconciliation_exception_details.csv")
print(OUTPUT_DIR / "reconciliation_exception_summary.csv")

engine.dispose()
