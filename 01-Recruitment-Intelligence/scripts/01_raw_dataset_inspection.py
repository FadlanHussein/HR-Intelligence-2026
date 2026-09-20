import pandas as pd


file_path = 'data/raw/recruitment_mydata.csv'
df = pd.read_csv(file_path)

print("Pandas berhasil telah dibaca!!")

print(" Jumlah baris dan kolom: ")
print(df.shape)

print(" Nama kolom")
print(df.columns.tolist())

print("\nTipe data setiap kolom")
print(df.dtypes)

print("\nDuplicate records:")
print(df.duplicated().sum())

print("\nStatistik data numerik")
print(df.describe())

print("\nUnique values - Gender:")
print(df["Gender"].unique())
print(df["Gender"].value_counts())

print("\nUnique values - EducationLevel:")
print(df["EducationLevel"].unique())
print(df["EducationLevel"].value_counts())

print("\nUnique values - RecruitmentStrategy:")
print(df["RecruitmentStrategy"].unique())
print(df["RecruitmentStrategy"].value_counts())

print("\nDistanceFromCompany:")
print("Min:", df["DistanceFromCompany"].min())
print("Max:", df["DistanceFromCompany"].max())
print("Unique values:", df["DistanceFromCompany"].nunique())

print("\nDistribusi HiringDecision:")
print(df["HiringDecision"].value_counts())

print ("\n" + "-" * 50)
print("Raw Dataset Inspection Summary")
print("-" * 50)

print(f"Total records    :  {len(df)}")
print(f"Total columns    :  {len(df.columns)}")
print(f"Missing cells    :  {df.isnull().sum().sum()}")
print(f"Duplicate rows   :  {df.duplicated().sum()}")


print("\nColumns:")
for column in df.columns:
    print(f"  {column}")

print("\nMissing values verification:")
print(df.isnull().sum())
print("\nTotal missing cells:")
print(df.isnull().sum().sum())
print("\nMissing values:")
print(df.isnull().sum())

print("\nMengecek Range Score:")
for col in ["InterviewScore", "SkillScore", "PersonalityScore"]:
    print(col, "| Min:", df[col].min(),
        "| Max:", df[col].max())

print("\nAnalisa Pengalaman Kerja:")
print("Min: ", df["ExperienceYears"].min())
print("Max: ", df["ExperienceYears"].max())
print("Unique Values:", df["ExperienceYears"].nunique())
print("Sample Values:", sorted(df["ExperienceYears"].dropna().unique())[:20])

print("\nPerusahaan Sebelumnya")
print("Min: ", df["PreviousCompanies"].min())
print("Max: ", df["PreviousCompanies"].max())
print("Unique Values:", df["PreviousCompanies"].nunique())
print("Sample Values:", sorted(df["PreviousCompanies"].dropna().unique())[:20])

print("\nHiringDecision:")
print("Min: ", df["HiringDecision"].min())
print("Max: ", df["HiringDecision"].max())
print("Unique Values:", df["HiringDecision"].nunique())
print("Sample Values:", sorted(df["HiringDecision"].dropna().unique())[:20])