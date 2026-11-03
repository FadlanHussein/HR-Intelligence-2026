import pandas as pd
import hashlib
import json
from sqlalchemy import create_engine, text
from pathlib import Path
from urllib.parse import quote_plus

# Project paths
BASE_DIR = Path(__file__).resolve().parent.parent

CSV_PATH = BASE_DIR / "data" / "test" / "recruitment_sync_test.csv"

# Database connection
DB_USER = "postgres"
DB_PASSWORD = quote_plus(input("Enter PostgreSQL password: "))
DB_HOST = "localhost"
DB_PORT = "5432"
DB_NAME = "recruitment_intelligence"

DATABASE_URL = (
    f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}"
    f"@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)

engine = create_engine(DATABASE_URL)

# Shared columns
SHARED_COLUMNS = [
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


def generate_fingerprint(row):
    values = []

    for value in row:
        if pd.isna(value):
            values.append(None)
        elif isinstance(value, str):
            values.append(" ".join(value.strip().casefold().split()))
        else:
            values.append(str(value))

    payload = json.dumps(values, ensure_ascii=False)

    return hashlib.sha256(payload.encode("utf-8")).hexdigest()
def insert_new_records(new_records, engine):
    inserted_count = 0
    skipped_count = 0

    insert_query = text("""
        INSERT INTO recruitment_candidates (
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
        )
        SELECT
            :age,
            :gender,
            :education_level,
            :experience_years,
            :previous_companies,
            :distance_from_company,
            :interview_score,
            :skill_score,
            :personality_score,
            :recruitment_strategy,
            :hiring_decision
        WHERE NOT EXISTS (
            SELECT 1
            FROM recruitment_candidates
            WHERE
                age = :age
                AND gender = :gender
                AND education_level = :education_level
                AND experience_years = :experience_years
                AND previous_companies = :previous_companies
                AND distance_from_company = :distance_from_company
                AND interview_score = :interview_score
                AND skill_score = :skill_score
                AND personality_score = :personality_score
                AND recruitment_strategy = :recruitment_strategy
                AND hiring_decision = :hiring_decision
        )
    """)

    with engine.begin() as connection:
        for _, row in new_records.iterrows():
            result = connection.execute(
                insert_query,
                row[SHARED_COLUMNS].to_dict()
            )

            if result.rowcount == 1:
                inserted_count += 1
            else:
                skipped_count += 1

    return inserted_count, skipped_count

# Read incoming CSV
incoming_df = pd.read_csv(CSV_PATH)

# Validate columns
missing_columns = set(SHARED_COLUMNS) - set(incoming_df.columns)

if missing_columns:
    raise ValueError(f"Missing columns: {missing_columns}")

incoming_df = incoming_df[SHARED_COLUMNS].copy()

# Read PostgreSQL records
database_df = pd.read_sql(
    text("""
        SELECT
            age, gender, education_level, experience_years,
            previous_companies, distance_from_company,
            interview_score, skill_score, personality_score,
            recruitment_strategy, hiring_decision
        FROM recruitment_candidates
    """),
    engine
)

# Generate fingerprints
incoming_df["fingerprint"] = incoming_df.apply(
    lambda row: generate_fingerprint(row[SHARED_COLUMNS]),
    axis=1
)

database_df["fingerprint"] = database_df.apply(
    lambda row: generate_fingerprint(row[SHARED_COLUMNS]),
    axis=1
)

# Detect new records
database_fingerprints = set(database_df["fingerprint"])

new_records = incoming_df[
    ~incoming_df["fingerprint"].isin(database_fingerprints)
]

print("\nDATA SYNCHRONIZATION CHECK")
print("-------------------------")
print(f"Incoming records : {len(incoming_df)}")
print(f"Database records : {len(database_df)}")
print(f"New records      : {len(new_records)}")
print(f"Existing records : {len(incoming_df) - len(new_records)}")

# Insert new records
inserted_count, skipped_count = insert_new_records(
    new_records,
    engine
)

print("\nINSERT RESULT")
print("-------------------------")
print(f"Inserted records : {inserted_count}")
print(f"Skipped records  : {skipped_count}")

# Close database connection
engine.dispose()