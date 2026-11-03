from pathlib import Path
import pandas as pd

# Project configuration
BASE_DIR = Path(__file__).resolve().parent.parent

SOURCE_PATH = (
    BASE_DIR / "data" / "raw" / "recruitment_mydata.csv"
)

TEST_DIR = BASE_DIR / "data" / "test"
TEST_DIR.mkdir(parents=True, exist_ok=True)

TEST_PATH = TEST_DIR / "recruitment_test.csv"

# Load original dataset
df = pd.read_csv(SOURCE_PATH)

# Introduce controlled data quality issues
df.loc[0, "Age"] = None
df.loc[1, "InterviewScore"] = 150
df.loc[2, "Gender"] = "Unknown"
df["ExperienceYears"] = df["ExperienceYears"].astype("object")
df.loc[3, "ExperienceYears"] = "Five years"

# Create a duplicate record
df = pd.concat(
    [df, df.iloc[[4]]],
    ignore_index=True
)

# Export test dataset
df.to_csv(TEST_PATH, index=False)

print("TEST DATASET CREATED")
print(f"Original records : {len(pd.read_csv(SOURCE_PATH))}")
print(f"Test records     : {len(df)}")
print(f"Test file        : {TEST_PATH}")
