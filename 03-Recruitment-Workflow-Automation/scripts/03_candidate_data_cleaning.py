from pathlib import Path
import pandas as pd
import re

# Project configuration
BASE_DIR = Path(__file__).resolve().parent.parent

SOURCE_PATH = (
    BASE_DIR / "data" / "raw" / "recruitment_mydata.csv"
)

OUTPUT_DIR = BASE_DIR / "data" / "processed"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

OUTPUT_PATH = (
    OUTPUT_DIR / "recruitment_candidates_clean.csv"
)

# Load raw dataset
df = pd.read_csv(SOURCE_PATH)

# Normalize column names
def normalize_column_name(column_name):
    column_name = re.sub(
        r"(?<!^)(?=[A-Z])",
        "_",
        column_name
    )
    return column_name.lower().strip()

df.columns = [
    normalize_column_name(column)
    for column in df.columns
]

print("\n=== RECRUITMENT DATA CLEANING ===")

print(f"Source records : {len(df)}")
print(f"Source columns : {len(df.columns)}")

print("\nRAW DATA SAMPLE")
print(df.head())

print("\nMISSING VALUES")
print(df.isnull().sum())

print("\nDATA TYPES")
print(df.dtypes)

# 1. Standardize text columns
TEXT_COLUMNS = [
    "gender",
    "education_level",
    "recruitment_strategy"
]

for column in TEXT_COLUMNS:
    df[column] = (
        df[column]
        .astype("string")
        .str.strip()
        .str.replace(r"\s+", " ", regex=True)
    )

# 2. Standardize category capitalization
df["gender"] = df["gender"].str.title()

EDUCATION_MAPPING = {
    "bachelor's (type 1)": "Bachelor's (Type 1)",
    "bachelor's (type 2)": "Bachelor's (Type 2)",
    "master's": "Master's",
    "phd": "PhD"
}

df["education_level"] = (
    df["education_level"]
    .str.lower()
    .map(EDUCATION_MAPPING)
    .fillna(df["education_level"])
)

df["recruitment_strategy"] = (
    df["recruitment_strategy"].str.title()
)

print("\nSTANDARDIZED CATEGORIES")

for column in TEXT_COLUMNS:
    print(f"\n{column}:")
    print(df[column].value_counts(dropna=False))

print("\nSTANDARDIZATION CHECK")

for column in TEXT_COLUMNS:
    print(f"{column}: {df[column].nunique()} unique categories")

print("\nEDUCATION LABEL CHECK")
print(df["education_level"].value_counts())

# 3. Missing Value Handling

NUMERIC_COLUMNS = [
    "age",
    "experience_years",
    "previous_companies",
    "distance_from_company",
    "interview_score",
    "skill_score",
    "personality_score"
]

CATEGORICAL_COLUMNS = [
    "gender",
    "education_level",
    "recruitment_strategy"
]

imputation_log = []

for column in NUMERIC_COLUMNS:
    missing_count = df[column].isna().sum()

    if missing_count > 0:
        median_value = df[column].median()
        df[column] = df[column].fillna(median_value)

        imputation_log.append({
            "column_name": column,
            "missing_values_filled": int(missing_count),
            "imputation_method": "Median",
            "replacement_value": median_value
        })

for column in CATEGORICAL_COLUMNS:
    missing_count = df[column].isna().sum()

    if missing_count > 0:
        mode_value = df[column].mode()[0]
        df[column] = df[column].fillna(mode_value)

        imputation_log.append({
            "column_name": column,
            "missing_values_filled": int(missing_count),
            "imputation_method": "Mode",
            "replacement_value": mode_value
        })

imputation_report = pd.DataFrame(
    imputation_log,
    columns=[
        "column_name",
        "missing_values_filled",
        "imputation_method",
        "replacement_value"
    ]
)

print("\nMISSING VALUE HANDLING")

if imputation_report.empty:
    print("No imputation required.")
else:
    print(imputation_report.to_string(index=False))

print("\nMISSING VALUES AFTER IMPUTATION")
print(df.isnull().sum())

# 4. Final Validation

print("\nFINAL DATA VALIDATION")

assert len(df) == 1493, "Record count changed unexpectedly"
assert df.isnull().sum().sum() == 0, "Missing values still exist"
assert df.columns.is_unique, "Duplicate column names detected"

print("Record count      : PASS")
print("Missing values    : PASS")
print("Unique columns    : PASS")

# 5. Export Clean Dataset

df.to_csv(OUTPUT_PATH, index=False)

imputation_report.to_csv(
    OUTPUT_DIR / "imputation_report.csv",
    index=False
)

print("\nEXPORT COMPLETED")
print(f"Clean dataset : {OUTPUT_PATH}")
print(f"Imputation log: {OUTPUT_DIR / 'imputation_report.csv'}")
print(f"Final records : {len(df)}")
print(f"Final columns : {len(df.columns)}")
