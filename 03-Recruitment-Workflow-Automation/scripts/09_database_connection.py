
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

# CREATE DATABASE ENGINE
engine = create_engine(DATABASE_URL)

print("\n=== POSTGRESQL CONNECTION TEST ===")

try:
    with engine.connect() as connection:

        result = connection.execute(
            text("SELECT current_database(), current_user")
        )

        database_info = result.fetchone()

        print("Connection status : SUCCESS")
        print(f"Database          : {database_info[0]}")
        print(f"User              : {database_info[1]}")

except SQLAlchemyError as error:
    print("Connection status : FAILED")
    print(f"Error             : {error}")

finally:
    engine.dispose()
