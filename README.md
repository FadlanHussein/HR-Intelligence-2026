# HR Intelligence 2026

Building data-driven HR solutions and automated workflows for smarter recruitment and talent decisions.

---

## 🚀 Repository Overview

This repository is the central workspace for the **HR Intelligence 2026** initiative. It houses end-to-end projects covering HR analytics, relational database modeling, business intelligence dashboards, and production-grade automated workflow pipelines with data quality assurance.

---

## 📁 Project Structure

```text
HR-Intelligence-2026/
├── 01-Recruitment-Intelligence/                  # Project 01: Analytics, SQL & Database
│   ├── scripts/                                  # Inspection, DB schema & Postgres import scripts
│   └── Sql/                                      # SQL fundamentals & business analytical queries
│       ├── Analysis/                             # Deep-dive recruitment SQL queries
│       └── Learning/                             # Core SQL exercises
├── 02-Data-Visualization-Business-Insight/       # Project 02: BI Dashboard & Visualization
│   └── dashboard/                               # Power BI reports (Recruitment_Intelligence.pbix)
├── 03-Recruitment-Workflow-Automation/           # Project 03: Automated Data Quality Gate & Pipeline
│   ├── data/
│   │   ├── processed/                           # Validation summaries & issue logs
│   │   ├── raw/                                 # Candidate dataset source
│   │   └── test/                                # Controlled anomaly test datasets
│   ├── documentation/                           # Project workflow documentation
│   ├── reports/                                 # Validation output reports
│   └── scripts/
│       ├── 01_candidate_data_validation.py      # Automated Data Quality Gate & issue logger
│       ├── 02_test_data_quality.py              # Controlled anomaly test generator
│       ├── 03_candidate_data_cleaning.py        # Candidate data cleaning & transformation
│       ├── 04_recruitment_workflow_automation.py # Candidate status mapping & workflow rules
│       └── 05_run_recruitment_pipeline.py       # End-to-end pipeline runner
├── data/
│   └── raw/                                     # Primary raw datasets (recruitment_mydata.csv)
├── docs/                                        # Global documentation
│   └── data_dictionary.md                       # Detailed dataset dictionary & quality rules
└── README.md
```

---

## 🛠️ Active Projects Summary

### 1. [01-Recruitment-Intelligence](./01-Recruitment-Intelligence/)
- **Objective:** Analyze 1,493 candidate records to understand hiring patterns, demographic distributions, and score impacts.
- **Tech Stack:** Python, PostgreSQL, SQL.
- **Key Deliverables:**
  - Relational schema modeling in PostgreSQL (`recruitment_candidates`).
  - 8 analytical SQL scripts assessing recruitment strategy, candidate quality, experience levels, and assessment score distributions.

### 2. [02-Data-Visualization-Business-Insight](./02-Data-Visualization-Business-Insight/)
- **Objective:** Build an interactive Executive Dashboard to surface recruitment metrics and business insights.
- **Tech Stack:** Power BI.
- **Key Deliverables:**
  - Interactive Power BI Executive Dashboard (`Recruitment_Intelligence.pbix`).

### 3. [03-Recruitment-Workflow-Automation](./03-Recruitment-Workflow-Automation/)
- **Objective:** Move from ad-hoc scripting to robust workflow automation by implementing an **Automated Data Quality Gate** and standardized data cleaning before downstream processing.
- **Tech Stack:** Python, Pandas, Regex, OS/Sys automation.
- **Key Features:**
  - **Dynamic Schema Normalization:** Converts incoming source columns (`PascalCase`) into standard `snake_case`.
  - **6-Layer Quality Validation:** Schema, Missing Values, Duplicate Records, Numeric Data Types, Range Violations, and Category Invariance.
  - **Unified Issue Logging:** Generates `data_quality_issue_log.csv` capturing row-level issues with assigned `issue_id` (e.g. `DQ-0001`), actual values, severity, and actionable descriptions.
  - **Process Control & Gate Decisions:** Employs standard process exit codes to halt or proceed in automated pipelines:
    - `0` (APPROVED / PASS) — Dataset passed all checks; safe for processing.
    - `1` (REJECTED / FAIL) — Critical data issues detected; pipeline execution blocked.
    - `2` (ON HOLD / WARNING) — Review required; pipeline paused for manual or triage review.
  - **Controlled Testing:** Synthetic anomaly generator (`02_test_data_quality.py`) to systematically verify all rejection and warning branches.

---

## 🚦 Automated Data Quality Gate Overview

| Check Layer | Verification Scope | Severity | Status If Failed |
| :--- | :--- | :--- | :--- |
| **Schema Validation** | 11 expected standardized columns present, no unexpected columns | CRITICAL | FAIL |
| **Missing Values** | Checks for null / NaN cells across all features | WARNING | WARNING |
| **Duplicate Records** | Identifies exact duplicate candidate rows | WARNING | WARNING |
| **Data Types** | Validates numeric casting for 8 quantitative columns | CRITICAL | FAIL |
| **Range Validation** | Bounds check (Age: 20-50, Exp: 0-15, Companies: 1-5, Scores: 0-100) | WARNING | WARNING |
| **Category Validation**| Verifies enum values for Gender, Strategy, and Hiring Decision | WARNING | WARNING |

All validation outputs are stored in `03-Recruitment-Workflow-Automation/data/processed/`.

---

## 🚀 Getting Started

### 1. Prerequisites & Environment Setup
Clone the repository and ensure Python 3.10+ and Pandas are installed:
```bash
git clone https://github.com/FadlanHussein/HR-Intelligence-2026.git
cd HR-Intelligence-2026
```

### 2. Run Data Quality Gate
To validate the production recruitment dataset:
```bash
python 03-Recruitment-Workflow-Automation/scripts/01_candidate_data_validation.py
```

### 3. Run Controlled Quality Anomaly Test
To simulate issues (missing values, invalid types, category errors, duplicates, out-of-range scores) and verify the gate blocks bad data:
```bash
# 1. Generate anomaly test data
python 03-Recruitment-Workflow-Automation/scripts/02_test_data_quality.py

# 2. Run validation against test dataset (expecting DECISION: REJECTED, Exit Code: 1)
```

---

## 📖 Documentation
Detailed variable descriptions, PostgreSQL mapping, validation ranges, and baseline recruitment metrics are documented in:
- [Data Dictionary & Quality Rules](docs/data_dictionary.md)

---

## 👤 Author
- **Fadlan Hussein**
- GitHub: [@FadlanHussein](https://github.com/FadlanHussein)
- Email: husseinfadlan16@gmail.com
