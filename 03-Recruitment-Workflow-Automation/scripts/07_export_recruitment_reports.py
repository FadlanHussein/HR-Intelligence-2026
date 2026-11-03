import pandas as pd
from pathlib import Path
from openpyxl.styles import Font, PatternFill, Alignment
from openpyxl.utils import get_column_letter

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data" / "processed"

# Load source data
summary_df = pd.read_csv(DATA_DIR / "recruitment_summary.csv")
strategy_df = pd.read_csv(DATA_DIR / "recruitment_strategy_summary.csv")
candidate_df = pd.read_csv(DATA_DIR / "candidate_status_report.csv")

# Calculate KPI
total_candidates = len(candidate_df)
hired_candidates = (candidate_df["candidate_status"] == "Hired").sum()
rejected_candidates = (candidate_df["candidate_status"] == "Rejected").sum()

hiring_rate = hired_candidates / total_candidates * 100
rejection_rate = rejected_candidates / total_candidates * 100

strategy_df["hiring_contribution"] = (
    strategy_df["hired_candidates"] / hired_candidates * 100
)

strategy_df["rejection_contribution"] = (
    strategy_df["rejected_candidates"] / rejected_candidates * 100
)

# Executive Summary
executive_df = pd.DataFrame({
    "KPI": [
        "Total Candidates",
        "Hired Candidates",
        "Rejected Candidates",
        "Hiring Rate (%)",
        "Rejection Rate (%)"
    ],
    "Value": [
        total_candidates,
        hired_candidates,
        rejected_candidates,
        round(hiring_rate, 2),
        round(rejection_rate, 2)
    ]
})

# Export Excel
excel_path = DATA_DIR / "recruitment_report.xlsx"

with pd.ExcelWriter(excel_path, engine="openpyxl") as writer:
    executive_df.to_excel(
        writer, sheet_name="Executive Summary", index=False
    )

    strategy_df.to_excel(
        writer, sheet_name="Strategy Performance", index=False
    )

    candidate_df.to_excel(
        writer, sheet_name="Candidate Details", index=False
    )

    workbook = writer.book

    for worksheet in workbook.worksheets:
        worksheet.freeze_panes = "A2"
        worksheet.auto_filter.ref = worksheet.dimensions

        for cell in worksheet[1]:
            cell.font = Font(bold=True, color="FFFFFF")
            cell.fill = PatternFill(
                fill_type="solid",
                fgColor="0A66C2"
            )
            cell.alignment = Alignment(horizontal="center")

        for column in worksheet.columns:
            max_length = max(
                len(str(cell.value or "")) for cell in column
            )
            column_letter = get_column_letter(column[0].column)
            worksheet.column_dimensions[column_letter].width = min(
                max_length + 3, 35
            )

# Export CSV KPI
csv_path = DATA_DIR / "recruitment_kpi_report.csv"

executive_df.to_csv(csv_path, index=False)

print("\n=== RECRUITMENT REPORT EXPORT ===")
print(f"Excel report: {excel_path}")
print(f"CSV report: {csv_path}")
print("Export status: COMPLETED")