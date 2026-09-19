# Data Dictionary — Recruitment Intelligence

## Dataset Overview

| Item | Value |
| :--- | :--- |
| **File Path** | `data/raw/recruitment_mydata.csv` |
| **Total Records** | 1,500 rows |
| **Total Columns** | 11 columns |
| **Missing Cells** | 7 cells (1 per column across 7 features) |
| **Duplicate Rows** | 0 rows |
| **Target Distribution** | Not Hired (0): 1,035 (69.0%) \| Hired (1): 465 (31.0%) |

---

## Variables

| Column | Data Type | Description | Expected Values / Range | Role |
| :--- | :--- | :--- | :--- | :--- |
| `Age` | `float64` | Usia kandidat pelamar | 20 – 50 tahun | Candidate Attribute |
| `Gender` | `str` | Jenis kelamin kandidat | `Female`, `Male` | Candidate Attribute |
| `EducationLevel` | `str` | Tingkat pendidikan formal terakhir | `Bachelor's (Type 1)`, `Bachelor's (Type 2)`, `Master's`, `PhD` | Candidate Attribute |
| `ExperienceYears` | `float64` | Lama pengalaman kerja profesional | 0 – 15 tahun | Candidate Attribute |
| `PreviousCompanies` | `int64` | Jumlah perusahaan tempat pernah bekerja | 1 – 5 perusahaan | Candidate Attribute |
| `DistanceFromCompany` | `float64` | Jarak tempat tinggal kandidat ke kantor | ~1.03 – 50.99 (km) | Candidate Attribute |
| `InterviewScore` | `float64` | Nilai hasil evaluasi sesi interview | 0 – 100 | Assessment Score |
| `SkillScore` | `float64` | Nilai uji keahlian / kemampuan teknis | 0 – 100 | Assessment Score |
| `PersonalityScore` | `float64` | Nilai evaluasi kepribadian / psikotes | 0 – 100 | Assessment Score |
| `RecruitmentStrategy` | `str` | Strategi pendekatan rekrutmen yang diterapkan | `Aggressive`, `Moderate`, `Conservative` | Recruitment Attribute |
| `HiringDecision` | `int64` | Keputusan akhir rekrutmen | `0` = Not Hired, `1` = Hired | Target / Outcome |

---

## Notes & Observations

- **Target Imbalance**: Sekitar 69% kandidat berstatus *Not Hired* dan 31% *Hired*.
- **Missing Values**: Terdapat 7 sel kosong (*NaN*) yang tersebar masing-masing 1 baris pada kolom: `Age`, `EducationLevel`, `ExperienceYears`, `InterviewScore`, `SkillScore`, `PersonalityScore`, dan `RecruitmentStrategy`.
- **Data Types**: Kolom numerik diskrit seperti `Age` dan `ExperienceYears` terbaca sebagai `float64` karena adanya nilai *NaN* pada data mentah.

