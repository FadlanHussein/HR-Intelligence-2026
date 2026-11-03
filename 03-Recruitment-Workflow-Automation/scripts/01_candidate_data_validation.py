from pathlib import Path
import re
import pandas as pd
import sys

# Lokasi project configuration
BASE_DIR = Path(__file__).resolve().parent.parent

# Lokasi data raw
DATA_PATH = BASE_DIR / "data" / "raw" / "recruitment_mydata.csv"
REPORT_DIR = BASE_DIR / "data" / "processed"
REPORT_DIR.mkdir(parents=True, exist_ok=True)

# 2. Struktur Data

EXPECTED_COLUMNS = [
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

# 3. Load Dataset

if not DATA_PATH.exists():
    raise FileNotFoundError(
        f"Dataset not found: {DATA_PATH}"
    )

df = pd.read_csv(DATA_PATH)

# Normalize column names into snake_case
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

print("\nNORMALIZED COLUMN NAMES")
print(df.columns.tolist())
print("\nDATASET SAMPLE")
print(df.head())
print("\nDATASET INFO")
df.info()

print("\n=== RECRUITMENT DATA VALIDATION ===")

print("\n[1] DATASET OVERVIEW")
print(f"Total rows      : {df.shape[0]}")
print(f"Total columns   : {df.shape[1]}")

# 4. Schema Validation

missing_columns = [
    column
    for column in EXPECTED_COLUMNS
    if column not in df.columns
]
unexpected_columns = [
    column
    for column in df.columns
    if column not in EXPECTED_COLUMNS
]

schema_valid = len(missing_columns) == 0

print("\n[2] SCHEMA VALIDATION")
print(f"Schema valid            : {schema_valid}")
print(f"Missing columns         : {missing_columns}")
print(f"Unexpected columns      : {unexpected_columns}")

# 5. Missing Value Validation

missing_summary = (
    df.isnull()
    .sum()
    .reset_index()
)

missing_summary.columns = [
    "column_name",
    "missing_count"
]

missing_summary = missing_summary[
    missing_summary["missing_count"] > 0
]

print("\n[3] MISSING VALUE VALIDATION")

if missing_summary.empty:
    print("No missing values found.")
else:
    print(missing_summary.to_string(index=False))

missing_summary.to_csv(
    REPORT_DIR / "missing_values_report.csv",
    index=False
)

# 6. Duplicate Validation

duplicate_count = df.duplicated().sum()

print("\n[4] DUPLICATE VALIDATION")
print(f"Duplicate rows: {duplicate_count}")

duplicate_records = df[df.duplicated(keep=False)]

duplicate_records.to_csv(
    REPORT_DIR / "duplicate_records_report.csv",
    index=False
)

# 7. Data Type Validation

print("\n[5] DATA TYPE VALIDATION")

type_results = []

for column in NUMERIC_COLUMNS:
    if column not in df.columns:
        continue

    converted = pd.to_numeric(
        df[column],
        errors="coerce"
    )

    invalid_count = (
        df[column].notna() & converted.isna()
    ).sum()

    type_results.append({
        "column_name": column,
        "invalid_numeric_count": int(invalid_count)
    })

type_report = pd.DataFrame(
    type_results,
    columns=[
        "column_name",
        "invalid_numeric_count"
    ]
)

print(type_report.to_string(index=False))

type_report.to_csv(
    REPORT_DIR / "data_type_report.csv",
    index=False
)

# 8. Range Validation

RANGE_RULES = {
    "age": (20, 50),
    "experience_years": (0, 15),
    "previous_companies": (1, 5),
    "distance_from_company": (0, 100),
    "interview_score": (0, 100),
    "skill_score": (0, 100),
    "personality_score": (0, 100),
    "hiring_decision": (0, 1)
}

range_issues = []

for column, (minimum, maximum) in RANGE_RULES.items():

    if column not in df.columns:
        continue

    numeric_values = pd.to_numeric(
        df[column],
        errors="coerce"
    )

    invalid_mask = (
        numeric_values.notna()
        & (
            (numeric_values < minimum)
            | (numeric_values > maximum)
        )
    )

    invalid_rows = df[invalid_mask].copy()

    for index, row in invalid_rows.iterrows():
        range_issues.append({
            "row_index": index,
            "candidate_id": row.get("candidate_id"),
            "column_name": column,
            "invalid_value": row[column],
            "minimum_allowed": minimum,
            "maximum_allowed": maximum
        })

range_report = pd.DataFrame(range_issues)

print("\n[6] RANGE VALIDATION")

if range_report.empty:
    print("No range violations found.")
else:
    print(range_report.to_string(index=False))

range_report.to_csv(
    REPORT_DIR / "range_validation_report.csv",
    index=False
)

# 9. Category Validation

CATEGORY_RULES = {
    "gender": ["Male", "Female"],
    "recruitment_strategy": [
        "Aggressive",
        "Moderate",
        "Conservative"
    ],
    "hiring_decision": [0, 1]
}

category_issues = []

for column, allowed_values in CATEGORY_RULES.items():
    if column not in df.columns:
        continue

    invalid_mask = (
        df[column].notna()
        & ~df[column].isin(allowed_values)
    )

    invalid_rows = df[invalid_mask]

    for index, row in invalid_rows.iterrows():
        category_issues.append({
            "row_index": index,
            "candidate_id": row.get("candidate_id"),
            "column_name": column,
            "invalid_value": row[column],
            "allowed_values": ", ".join(
                map(str, allowed_values)
            )
        })
category_report = pd.DataFrame(category_issues)
print("\n[7] CATEGORY VALIDATION")

if category_report.empty:
    print("No Invalid categories Found.")
else:
    print(category_report.to_string(index=False))

category_report.to_csv(
    REPORT_DIR / "category_validation_report.csv",
    index=False
)

# 10. Final Validation Summary

missing_total = int(df.isnull().sum().sum())

duplicate_total = int(duplicate_count)

invalid_numeric_total = int(
    type_report["invalid_numeric_count"].sum()
)

range_issue_total = len(range_report)
category_issue_total = len(category_report)

schema_issue_total = (
    len(missing_columns) + len(unexpected_columns)
)

# Define validation checks
validation_checks = [
    {
        "check_name": "Schema Validation",
        "issue_count": schema_issue_total,
        "severity": "CRITICAL"
    },
    {
        "check_name": "Missing Value Validation",
        "issue_count": missing_total,
        "severity": "WARNING"
    },
    {
        "check_name": "Duplicate Validation",
        "issue_count": duplicate_total,
        "severity": "WARNING"
    },
    {
        "check_name": "Data Type Validation",
        "issue_count": invalid_numeric_total,
        "severity": "CRITICAL"
    },
    {
        "check_name": "Range Validation",
        "issue_count": range_issue_total,
        "severity": "WARNING"
    },
    {
        "check_name": "Category Validation",
        "issue_count": category_issue_total,
        "severity": "WARNING"
    }
]

# Determine status for each check
for check in validation_checks:

    if check["issue_count"] == 0:
        check["status"] = "PASS"

    elif check["severity"] == "CRITICAL":
        check["status"] = "FAIL"

    else:
        check["status"] = "WARNING"


# Convert results into DataFrame
validation_report = pd.DataFrame(validation_checks)

# Determine overall status
if "FAIL" in validation_report["status"].values:
    overall_status = "FAIL"

elif "WARNING" in validation_report["status"].values:
    overall_status = "WARNING"

else:
    overall_status = "PASS"



# 11. Display Final Report

print("\n=== CONSOLIDATED VALIDATION REPORT ===")

print(f"Dataset       : {DATA_PATH.name}")
print(f"Total records : {len(df)}")
print(f"Total columns : {len(df.columns)}")

print("\nVALIDATION RESULTS")
print(validation_report.to_string(index=False))

print(f"\nOVERALL STATUS: {overall_status}")


# 12. Export Consolidated Report

validation_report.to_csv(
    REPORT_DIR / "consolidated_validation_report.csv",
    index=False
)

# Export overall status separately
overall_report = pd.DataFrame([{
    "dataset_name": DATA_PATH.name,
    "total_records": len(df),
    "total_columns": len(df.columns),
    "overall_status": overall_status
}])

overall_report.to_csv(
    REPORT_DIR / "overall_validation_status.csv",
    index=False
)

print("\nReports successfully exported.")
print(f"Output directory: {REPORT_DIR}")


# 13. DATA QUALITY ISSUE LOGGING

issue_records = []

# A. MISSING VALUE ISSUES

for column in df.columns:
    missing_rows = df[df[column].isna()]
    for index, row in missing_rows.iterrows():
        issue_records.append({
            "row_index": index,
            "column_name": column,
            "issue_type": "Missing Value",
            "actual_value": None,
            "severity": "WARNING",
            "description": f"{column} contains an empty value"
        })

# B. DUPLICATE ISSUES

duplicate_rows = df[df.duplicated(keep=False)]
for index, row in duplicate_rows.iterrows():
    issue_records.append({
        "row_index": index,
        "column_name": "all_columns",
        "issue_type": "Duplicate Record",
        "actual_value": "duplicate_row",
        "severity": "WARNING",
        "description": "Entire row is duplicated"
    })

# C. DATA TYPE ISSUES

for column in NUMERIC_COLUMNS:
    if column not in df.columns:
        continue

    converted = pd.to_numeric(
        df[column],
        errors="coerce"
    )

    invalid_mask = df[column].notna() & converted.isna()
    invalid_rows = df[invalid_mask]

    for index, row in invalid_rows.iterrows():
        issue_records.append({
            "row_index": index,
            "column_name": column,
            "issue_type": "Invalid Data Type",
            "actual_value": row[column],
            "severity": "CRITICAL",
            "description": f"{column} has non-numeric value: {row[column]}"
        })

# D. RANGE ISSUES

for item in range_issues:
    issue_records.append({
        "row_index": item["row_index"],
        "column_name": item["column_name"],
        "issue_type": "Out of Range",
        "actual_value": item["invalid_value"],
        "severity": "WARNING",
        "description": f"{item['column_name']} value {item['invalid_value']} is outside allowed range ({item['minimum_allowed']} - {item['maximum_allowed']})"

    })

# E. CATEGORY ISSUES

for item in category_issues:
    issue_records.append({
        "row_index": item["row_index"],
        "column_name": item["column_name"],
        "issue_type": "Invalid Category",
        "actual_value": item["invalid_value"],
        "severity": "WARNING",
        "description": f"{item['column_name']} value '{item['invalid_value']}' is not in allowed categories ({item['allowed_values']})"
    })

# F. SCHEMA ISSUES

for column in missing_columns:
    issue_records.append({
        "row_index": None,
        "column_name": column,
        "issue_type": "Missing Column",
        "actual_value": None,
        "severity": "CRITICAL",
        "description": f"Expected column '{column}' is missing from dataset"
    })

for column in unexpected_columns:
    issue_records.append({
        "row_index": None,
        "column_name": column,
        "issue_type": "Unexpected Column",
        "actual_value": None,
        "severity": "WARNING",
        "description": f"Unexpected column '{column}' found in dataset"
    })

# Convert to DataFrame
issue_columns = [
    "issue_id",
    "row_index",
    "column_name",
    "issue_type",
    "actual_value",
    "severity",
    "description"
]

if issue_records:
    issue_log = pd.DataFrame(issue_records)
    issue_log.insert(
        0,
        "issue_id",
        [f"DQ-{i+1:04d}" for i in range(len(issue_log))]
    )
    issue_log = issue_log[issue_columns]
else:
    issue_log = pd.DataFrame(columns=issue_columns)

print("\n=== DATA QUALITY ISSUE LOG ===")
print(f"Total issues: {len(issue_log)}")

if issue_log.empty:
    print("No data quality issues detected.")
else:
    print("\nISSUE SUMMARY BY TYPE:")
    print(issue_log["issue_type"].value_counts().to_string())
    print("\nISSUE SUMMARY BY SEVERITY:")
    print(issue_log["severity"].value_counts().to_string())
    print("\nDETAILED ISSUES (FIRST 10):")
    print(issue_log.head(10).to_string(index=False))

# Export issue log
issue_log.to_csv(
    REPORT_DIR / "data_quality_issue_log.csv",
    index=False
)

print("\nIssue log exported successfully.")

# 14. Automated Data Quality Gate

print("\n=== AUTOMATED DATA QUALITY GATE ===")


if overall_status == "PASS":

    print("DECISION: APPROVED")
    print("Dataset passed all validation checks.")
    print("Next process is allowed to continue.")

    exit_code = 0

elif overall_status == "WARNING":

    print("DECISION: ON HOLD")
    print("Dataset contains issues that require review.")
    print("Please review the validation reports.")
    
    exit_code = 2

else:

    print("DECISION: REJECTED")
    print("Critical data quality issues detected.")
    print("Further processing is blocked.")

    exit_code = 1


print(f"\nProcess exit code: {exit_code}")

sys.exit(exit_code)