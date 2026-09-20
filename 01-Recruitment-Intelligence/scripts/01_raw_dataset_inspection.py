import pandas as pd


# 1. LOAD DATASET
file_path = 'data/raw/recruitment_mydata.csv'
df = pd.read_csv(file_path)

print("Pandas berhasil membaca dataset!")


# 2. TASK 1.1 - RAW DATASET INSPECTION
print("\nJumlah baris dan kolom:")
print(df.shape)

print("\nNama kolom:")
print(df.columns.tolist())

print("\nTipe data setiap kolom:")
print(df.dtypes)

print("\nDuplicate records:")
print(df.duplicated().sum())

print("\nStatistik data numerik:")
print(df.describe())


# 3. CATEGORICAL INSPECTION
print("\nUnique values - Gender:")
print(df["Gender"].unique())
print(df["Gender"].value_counts())

print("\nUnique values - EducationLevel:")
print(df["EducationLevel"].unique())
print(df["EducationLevel"].value_counts())

print("\nUnique values - RecruitmentStrategy:")
print(df["RecruitmentStrategy"].unique())
print(df["RecruitmentStrategy"].value_counts())


# 4. DISTANCE FROM COMPANY
print("\nDistanceFromCompany:")
print("Min:", df["DistanceFromCompany"].min())
print("Max:", df["DistanceFromCompany"].max())
print("Unique values:", df["DistanceFromCompany"].nunique())


# 5. HIRING DECISION INSPECTION
print("\nDistribusi HiringDecision:")
print(df["HiringDecision"].value_counts())


# 6. RAW DATASET SUMMARY
print("\n" + "-" * 50)
print("Raw Dataset Inspection Summary")
print("-" * 50)

print(f"Total records   : {len(df)}")
print(f"Total columns   : {len(df.columns)}")
print(f"Missing cells   : {df.isnull().sum().sum()}")
print(f"Duplicate rows  : {df.duplicated().sum()}")

print("\nColumns:")
for column in df.columns:
    print(f"  {column}")


# 7. TASK 1.3 - DATA QUALITY CHECK
print("\n" + "-" * 50)
print("TASK 1.3 - DATA QUALITY CHECK")
print("-" * 50)

# 1. Missing Values
print("\nMissing values verification:")
print(df.isna().sum())
print("\nTotal Missing Cells:", df.isna().sum().sum())

# 2. Range Inspection (Scores)
print("\nPengecekan Range Score:")
for col in ["InterviewScore", "SkillScore", "PersonalityScore"]:
    print(col, "| Min:", df[col].min(), "| Max:", df[col].max())

# 3. Experience Years
print("\nAnalisa Pengalaman Kerja:")
print("Min:", df["ExperienceYears"].min())
print("Max:", df["ExperienceYears"].max())
print("Unique Values:", df["ExperienceYears"].nunique())
print("Sample Values:", sorted(df["ExperienceYears"].dropna().unique())[:20])

# 4. Previous Companies
print("\nPerusahaan Sebelumnya:")
print("Min:", df["PreviousCompanies"].min())
print("Max:", df["PreviousCompanies"].max())
print("Unique Values:", df["PreviousCompanies"].nunique())
print("Sample Values:", sorted(df["PreviousCompanies"].dropna().unique())[:20])

# 5. Hiring Decision
print("\nHiringDecision:")
print("Min:", df["HiringDecision"].min())
print("Max:", df["HiringDecision"].max())
print("Unique Values:", df["HiringDecision"].nunique())
print("Sample Values:", sorted(df["HiringDecision"].dropna().unique())[:20])

# 6. Range Validity Check
print("\nPengecekan validitas data (Out of Range):")

checks = {
    # Age harus berada pada range 20–50
    "Age": (df["Age"] < 20) | (df["Age"] > 50),

    # ExperienceYears harus berada pada range 0–15
    "ExperienceYears": (df["ExperienceYears"] < 0) | (df["ExperienceYears"] > 15),

    # PreviousCompanies harus berada pada range 1–5
    "PreviousCompanies": (df["PreviousCompanies"] < 1) | (df["PreviousCompanies"] > 5),

    # Score harus berada pada range 0–100
    "InterviewScore": (df["InterviewScore"] < 0) | (df["InterviewScore"] > 100),
    "SkillScore": (df["SkillScore"] < 0) | (df["SkillScore"] > 100),
    "PersonalityScore": (df["PersonalityScore"] < 0) | (df["PersonalityScore"] > 100),

    # HiringDecision hanya boleh 0 atau 1
    "HiringDecision": ~df["HiringDecision"].isin([0, 1])
}

for column, condition in checks.items():
    print(f"  {column:<20}: {condition.sum()} invalid values")