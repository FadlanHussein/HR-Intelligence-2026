
import pandas as pd
from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError

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

print("\n=== RECRUITMENT DATABASE READING ===")

try:
    with engine.connect() as connection:

        # 1. COUNT TOTAL CANDIDATES
        count_query = text("""
            SELECT COUNT(*)
            FROM recruitment_candidates
        """)

        total_candidates = connection.execute(
            count_query
        ).scalar_one()

        print(f"\nTotal candidates: {total_candidates}")

        # 2. READ SAMPLE CANDIDATE DATA
        sample_query = text("""
            SELECT
                candidate_id,
                age,
                gender,
                education_level,
                experience_years,
                interview_score,
                skill_score,
                personality_score,
                hiring_decision
            FROM recruitment_candidates
            ORDER BY candidate_id
            LIMIT 5
        """)

        df = pd.read_sql(
            sample_query,
            connection
        )

        print("\n=== CANDIDATE DATA SAMPLE ===")
        print(df.to_string(index=False))

        # 3. DATAFRAME INFORMATION
        print("\n=== DATAFRAME INFORMATION ===")
        print(f"Rows    : {len(df)}")
        print(f"Columns : {len(df.columns)}")

        print("\n=== DATA TYPES ===")
        print(df.dtypes)

        print("\nDatabase reading: SUCCESS")

except SQLAlchemyError as error:
    print("\nDatabase reading: FAILED")
    print(f"Error: {error}")

finally:
    engine.dispose()
