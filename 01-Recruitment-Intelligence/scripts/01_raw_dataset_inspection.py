import pandas as pd


file_path = 'data/raw/recruitment_mydata.csv'
df = pd.read_csv(file_path)

print("Pandas berhasil telah dibaca!!")

print(" Jumlah baris dan kolom: ")
print(df.shape)

print(" Nama kolom")
print(df.columns.tolist())

print("\nsample 10 data pertama: ")
print(df.head(10))

print("\nTipe data setiap kolom")
print(df.dtypes)

print("\nMissing values:")
print(df.isnull().sum())

print("\nDuplicate records:")
print(df.duplicated().sum())

print("\nStatistik data numerik")
print(df.describe())

print("\nUnique values - Gender:")
print(df["Gender"].unique())

print("\nUnique values - EducationLevel:")
print(df["EducationLevel"].unique())

print("\nUnique values - RecruitmentStrategy:")
print(df["RecruitmentStrategy"].unique())

print("\nDistribusi HiringDecision:")
print(df["HiringDecision"].value_counts())

print ("\n" + "-" * 50)
print("Raw Dataset Inspection Summary")
print("-" * 50)

print(f"Total records    :  {len(df)}")
print(f"Total columns    :  {len(df.columns)}")
print(f"Missing cells    :  {df.duplicated().sum()}")


print("\nColumns:")
for column in df.columns:
    print(f"  {column}")

print("\nMissing values verification:")
print(df.isnull().sum())

print("\nTotal missing cells:")
print(df.isnull().sum().sum())
