
from pathlib import Path
import pandas as pd
from sqlalchemy import create_engine, text

# PROJECT PATH
BASE_DIR = Path(__file__).resolve().parent.parent

CSV_FILE = (
    BASE_DIR
    / "data"
    / "processed"
    / "recruitment_candidates_clean.csv"
)

# DATABASE CONFIGURATION
DB_USER = "postgres"
DB_PASSWORD = "ISI_PASSWORD_POSTGRESQL"
DB_HOST = "localhost"
DB_PORT = "5432"
DB_NAME = "recruitment_intelligence"

DATABASE_URL = (
    f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}"
    f"@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)

engine = create_engine(DATABASE_URL)

print("\n=== RECRUITMENT DATA RECONCILIATION ===")

try:
    # 1. READ CSV DATA
    csv_df = pd.read_csv(CSV_FILE)

    csv_total = len(csv_df)
    csv_hired = (csv_df["hiring_decision"] == 1).sum()
    csv_rejected = (csv_df["hiring_decision"] == 0).sum()

    # 2. READ DATABASE SUMMARY
    database_query = text("""
        SELECT
            COUNT(*) AS total_candidates,
            COUNT(*) FILTER (
                WHERE hiring_decision = 1
            ) AS hired_candidates,
            COUNT(*) FILTER (
                WHERE hiring_decision = 0
            ) AS rejected_candidates
        FROM recruitment_candidates
    """)

    with engine.connect() as connection:
        db_result = connection.execute(
            database_query
        ).mappings().one()

    db_total = db_result["total_candidates"]
    db_hired = db_result["hired_candidates"]
    db_rejected = db_result["rejected_candidates"]

    # 3. RECONCILIATION COMPARISON
    comparisons = [
        {
            "metric": "Total Candidates",
            "csv_value": csv_total,
            "database_value": db_total
        },
        {
            "metric": "Hired Candidates",
            "csv_value": csv_hired,
            "database_value": db_hired
        },
        {
            "metric": "Rejected Candidates",
            "csv_value": csv_rejected,
            "database_value": db_rejected
        }
    ]

    report = pd.DataFrame(comparisons)

    report["difference"] = (
        report["database_value"] - report["csv_value"]
    )

    report["status"] = report["difference"].apply(
        lambda value: "MATCH" if value == 0 else "MISMATCH"
    )

    # 4. DISPLAY RESULTS
    print("\n=== SOURCE COMPARISON ===")
    print(report.to_string(index=False))

    # 5. OVERALL STATUS
    overall_status = (
        "MATCH"
        if (report["status"] == "MATCH").all()
        else "MISMATCH"
    )

    print(f"\nOverall reconciliation: {overall_status}")

    # 6. EXPORT REPORT
    output_file = (
        BASE_DIR
        / "data"
        / "processed"
        / "recruitment_reconciliation_report.csv"
    )

    report.to_csv(output_file, index=False)

    print(f"Report saved: {output_file}")

except Exception as error:
    print("\nReconciliation failed.")
    print(f"Error: {error}")

finally:
    engine.dispose()
