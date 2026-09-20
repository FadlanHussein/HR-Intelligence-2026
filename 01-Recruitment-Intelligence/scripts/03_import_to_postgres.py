import pandas as pd

file_path = 'data/raw/recruitment_mydata.csv'

df = pd.read_csv(file_path)

print("Dataset berhasil dibaca!")
print("Shape:", df.shape)

print("\n5 data pertama:")
print(df.head())

df.columns = [
    'age',
    'gender',
    'education_level',
    'experience_years',
    'previous_companies',
    'distance_from_company',
    'interview_score',
    'skill_score',
    'personality_score',
    'recruitment_strategy',
    'hiring_decision'
]

int_cols = [
    'age',
    'experience_years',
    'interview_score',
    'skill_score',
    'personality_score'
]

for col in int_cols:
    df[col] = df[col].astype('Int64')

print("\nTipe data setelah transformasi:")
print(df.dtypes)

print("\nMissing values:")
print(df.isna().sum())

print("\nTotal missing cells:", df.isna().sum().sum())

print("\n5 data setelah transformasi:")
print(df.head())

print("\nETL Checkpoint")
print("Extract  : OK")
print("Transform: OK")
print("Load     : NOT YET")
print("Rows     :", len(df))
print("Columns  :", len(df.columns))

from sqlalchemy import create_engine, URL
from getpass import getpass

password = getpass("Masukkan password PostgreSQL: ")

connection_url = URL.create(
    "postgresql+psycopg2",
    username="postgres",
    password=password,
    host="localhost",
    port=5432,
    database="recruitment_intelligence"
)

engine = create_engine(connection_url)

df = df.astype(object).where(pd.notna(df), None)

df.to_sql(
    "recruitment_candidates",
    engine,
    if_exists="append",
    index=False,
    method="multi"
)

print("\nData berhasil dimasukkan ke PostgreSQL!")
print("Rows loaded:", len(df))