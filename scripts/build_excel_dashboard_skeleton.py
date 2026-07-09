"""
Build an Excel workbook skeleton for the LNG Operations Technical Reliability Dashboard.

The workbook is a starter dashboard for portfolio demonstration. It uses public
industrial datasets adapted into LNG-style reliability categories. It does not
use ExxonMobil or PNG LNG operating data.

Inputs:
- data/processed/azure_machine_reliability_summary.csv
- data/processed/phmsa_incident_risk_summary.csv
- samples/metropt3/metropt3_compressor_sample.csv

Outputs:
- excel/lng_operations_reliability_dashboard.xlsx
- reports/excel_dashboard_build_report.md

Run from the project root:
    python scripts\\build_excel_dashboard_skeleton.py
"""

from __future__ import annotations

from datetime import datetime
from pathlib import Path

try:
    import pandas as pd
    from openpyxl import Workbook
    from openpyxl.chart import BarChart, LineChart, Reference
    from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
    from openpyxl.utils import get_column_letter
    from openpyxl.utils.dataframe import dataframe_to_rows
    from openpyxl.worksheet.table import Table, TableStyleInfo
except ImportError as error:
    raise SystemExit(
        "This script requires pandas and openpyxl. Install them with:\n"
        "pip install pandas openpyxl\n\n"
        "Or install all project dependencies with:\n"
        "pip install -r requirements.txt"
    ) from error


PROJECT_ROOT = Path(__file__).resolve().parents[1]

AZURE_INPUT_PATH = (
    PROJECT_ROOT / "data" / "processed" / "azure_machine_reliability_summary.csv"
)
PHMSA_INPUT_PATH = (
    PROJECT_ROOT / "data" / "processed" / "phmsa_incident_risk_summary.csv"
)
METROPT3_INPUT_PATH = (
    PROJECT_ROOT / "samples" / "metropt3" / "metropt3_compressor_sample.csv"
)

WORKBOOK_OUTPUT_PATH = (
    PROJECT_ROOT / "excel" / "lng_operations_reliability_dashboard.xlsx"
)
REPORT_OUTPUT_PATH = PROJECT_ROOT / "reports" / "excel_dashboard_build_report.md"

REQUIRED_INPUTS = [
    AZURE_INPUT_PATH,
    PHMSA_INPUT_PATH,
    METROPT3_INPUT_PATH,
]

# Simple workbook colors.
NAVY_FILL = PatternFill("solid", fgColor="1F4E78")
BLUE_FILL = PatternFill("solid", fgColor="D9EAF7")
LIGHT_FILL = PatternFill("solid", fgColor="F3F6FA")
GREEN_FILL = PatternFill("solid", fgColor="D9EAD3")
AMBER_FILL = PatternFill("solid", fgColor="FCE5CD")
RED_FILL = PatternFill("solid", fgColor="F4CCCC")
WHITE_FONT = Font(color="FFFFFF", bold=True)
BOLD_FONT = Font(bold=True)
TITLE_FONT = Font(size=16, bold=True, color="1F4E78")
SUBTITLE_FONT = Font(size=11, italic=True, color="666666")
THIN_BORDER = Border(
    left=Side(style="thin", color="D9E2F3"),
    right=Side(style="thin", color="D9E2F3"),
    top=Side(style="thin", color="D9E2F3"),
    bottom=Side(style="thin", color="D9E2F3"),
)


def check_required_inputs() -> None:
    """Stop early with a clear message if a dashboard input file is missing."""
    missing_files = [path for path in REQUIRED_INPUTS if not path.exists()]

    if not missing_files:
        return

    print("Missing required dashboard input file(s):")
    for path in missing_files:
        print(f"- {path.relative_to(PROJECT_ROOT)}")

    raise SystemExit(
        "Run the data inspection and processing scripts first, then rerun this script."
    )


def read_dashboard_inputs() -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """Read the processed and sample CSV files used by the workbook."""
    print("Reading dashboard input files...")
    azure = pd.read_csv(AZURE_INPUT_PATH)
    phmsa = pd.read_csv(PHMSA_INPUT_PATH)
    metropt3 = pd.read_csv(METROPT3_INPUT_PATH)
    return azure, phmsa, metropt3


def safe_sheet_title(title: str) -> str:
    """Keep worksheet titles within Excel's 31-character limit."""
    return title[:31]


def apply_title(ws, title: str, subtitle: str | None = None) -> None:
    """Add a consistent title block to a worksheet."""
    ws["A1"] = title
    ws["A1"].font = TITLE_FONT
    if subtitle:
        ws["A2"] = subtitle
        ws["A2"].font = SUBTITLE_FONT
        ws["A2"].alignment = Alignment(wrap_text=True)


def set_column_widths(ws, min_width: int = 12, max_width: int = 42) -> None:
    """Auto-size columns with a cap so long notes do not make sheets unusable."""
    for column_cells in ws.columns:
        column_letter = get_column_letter(column_cells[0].column)
        max_length = 0

        for cell in column_cells:
            if cell.value is None:
                continue
            max_length = max(max_length, len(str(cell.value)))

        adjusted_width = min(max(max_length + 2, min_width), max_width)
        ws.column_dimensions[column_letter].width = adjusted_width


def style_range_as_grid(ws, start_row: int, end_row: int, start_col: int, end_col: int) -> None:
    """Apply simple borders and alignment to a cell range."""
    for row in ws.iter_rows(
        min_row=start_row, max_row=end_row, min_col=start_col, max_col=end_col
    ):
        for cell in row:
            cell.border = THIN_BORDER
            cell.alignment = Alignment(vertical="top", wrap_text=True)


def format_number_columns(ws, header_row: int, data_start_row: int) -> None:
    """Apply basic number formats based on column names."""
    for cell in ws[header_row]:
        header = str(cell.value).lower() if cell.value is not None else ""
        column_letter = get_column_letter(cell.column)

        if any(word in header for word in ["count", "records", "year"]):
            number_format = "#,##0"
        elif "percent" in header or "score" in header:
            number_format = "0.0"
        elif any(word in header for word in ["cost", "downtime", "hours"]):
            number_format = "#,##0.0"
        elif any(word in header for word in ["avg", "temperature", "pressure", "current"]):
            number_format = "0.00"
        else:
            continue

        for row_number in range(data_start_row, ws.max_row + 1):
            ws[f"{column_letter}{row_number}"].number_format = number_format


def write_dataframe_sheet(ws, dataframe: pd.DataFrame, table_name: str) -> None:
    """Write a dataframe to a worksheet and format it as an Excel table."""
    for row in dataframe_to_rows(dataframe, index=False, header=True):
        ws.append(row)

    ws.freeze_panes = "A2"
    ws.auto_filter.ref = ws.dimensions

    for header_cell in ws[1]:
        header_cell.fill = NAVY_FILL
        header_cell.font = WHITE_FONT
        header_cell.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)

    style_range_as_grid(ws, 1, ws.max_row, 1, ws.max_column)
    format_number_columns(ws, header_row=1, data_start_row=2)

    if ws.max_row >= 2 and ws.max_column >= 1:
        last_cell = f"{get_column_letter(ws.max_column)}{ws.max_row}"
        table = Table(displayName=table_name, ref=f"A1:{last_cell}")
        table.tableStyleInfo = TableStyleInfo(
            name="TableStyleMedium2",
            showFirstColumn=False,
            showLastColumn=False,
            showRowStripes=True,
            showColumnStripes=False,
        )
        ws.add_table(table)

    set_column_widths(ws)


def create_readme_sheet(wb: Workbook) -> None:
    """Create the README sheet with purpose, sources, and honesty wording."""
    ws = wb.create_sheet("README")
    apply_title(ws, "LNG Operations Technical Reliability Dashboard")

    rows = [
        ("Workbook purpose", "Starter Excel dashboard skeleton for operations technical reliability analysis."),
        (
            "Portfolio demonstration",
            "This workbook uses public industrial datasets adapted into LNG-style reliability categories.",
        ),
        (
            "Data integrity note",
            "No ExxonMobil or PNG LNG operating data is used. No confidential, proprietary, or licensee data is included.",
        ),
        ("Workbook status", "Dashboard starter/skeleton, not a final polished dashboard and not a live plant dashboard."),
        ("Data source 1", "Azure Predictive Maintenance"),
        ("Data source 2", "MetroPT-3 Compressor Dataset"),
        ("Data source 3", "PHMSA LNG/Gas Transmission Incident Data"),
        (
            "Generated on",
            datetime.now().strftime("%Y-%m-%d %H:%M"),
        ),
    ]

    ws.append([])
    ws.append(["Topic", "Details"])
    for topic, details in rows:
        ws.append([topic, details])

    for cell in ws[3]:
        cell.fill = NAVY_FILL
        cell.font = WHITE_FONT
    style_range_as_grid(ws, 3, ws.max_row, 1, 2)
    ws.column_dimensions["A"].width = 26
    ws.column_dimensions["B"].width = 95
    ws.freeze_panes = "A4"


def create_kpi_calculations_sheet(
    wb: Workbook, azure: pd.DataFrame, phmsa: pd.DataFrame, metropt3: pd.DataFrame
) -> dict[str, object]:
    """Create the KPI_Calculations sheet and return values for the dashboard."""
    ws = wb.create_sheet("KPI_Calculations")
    apply_title(ws, "KPI Calculations", "Formula guidance plus current calculated values.")

    total_assets = len(azure)
    critical_assets = int((azure["maintenance_priority"] == "Critical").sum())
    high_priority_assets = int((azure["maintenance_priority"] == "High").sum())
    average_health = round(float(azure["asset_health_score"].mean()), 1)
    total_downtime = round(float(azure["estimated_downtime_hours"].sum()), 1)
    phmsa_records = int(phmsa["incident_count"].sum()) if "incident_count" in phmsa.columns else len(phmsa)
    metropt3_records = len(metropt3)

    kpis = [
        (
            "total_assets",
            "=ROWS(tblAzureReliabilitySummary[machineID])",
            total_assets,
            "Count of Azure machines mapped into LNG-style assets.",
        ),
        (
            "critical_assets",
            '=COUNTIF(tblAzureReliabilitySummary[maintenance_priority],"Critical")',
            critical_assets,
            "Assets with Critical maintenance priority.",
        ),
        (
            "high_priority_assets",
            '=COUNTIF(tblAzureReliabilitySummary[maintenance_priority],"High")',
            high_priority_assets,
            "Assets with High maintenance priority.",
        ),
        (
            "average_asset_health_score",
            "=ROUND(AVERAGE(tblAzureReliabilitySummary[asset_health_score]),1)",
            average_health,
            "Average 0-100 screening score from the Azure reliability summary.",
        ),
        (
            "total_estimated_downtime_hours",
            "=SUM(tblAzureReliabilitySummary[estimated_downtime_hours])",
            total_downtime,
            "Failure count multiplied by the 8-hour downtime assumption.",
        ),
        (
            "phmsa_incident_risk_records",
            "=SUM(tblPHMSAIncidentRisk[incident_count])",
            phmsa_records,
            "Total PHMSA incident records represented by the grouped risk summary.",
        ),
        (
            "metropt3_sample_records",
            "=ROWS(tblMetroPT3CompressorSample[timestamp])",
            metropt3_records,
            "Rows in the GitHub-safe MetroPT-3 compressor sample.",
        ),
    ]

    ws.append([])
    kpi_header_row = ws.max_row + 1
    ws.append(["KPI", "Suggested Excel Formula", "Current Value", "Notes"])
    for row in kpis:
        ws.append(list(row))

    for cell in ws[kpi_header_row]:
        cell.fill = NAVY_FILL
        cell.font = WHITE_FONT
    style_range_as_grid(ws, kpi_header_row, kpi_header_row + len(kpis), 1, 4)

    # Helper table 1: maintenance priority count.
    priority_start_row = 13
    ws.cell(priority_start_row, 1, "Maintenance Priority")
    ws.cell(priority_start_row, 2, "Asset Count")
    priority_summary = (
        azure.groupby("maintenance_priority")
        .size()
        .reindex(["Critical", "High", "Medium", "Low"])
        .dropna()
        .astype(int)
    )
    for offset, (priority, count) in enumerate(priority_summary.items(), start=1):
        ws.cell(priority_start_row + offset, 1, priority)
        ws.cell(priority_start_row + offset, 2, int(count))

    # Helper table 2: average health by LNG equipment category.
    category_start_row = 13
    category_start_col = 4
    ws.cell(category_start_row, category_start_col, "LNG Equipment Category")
    ws.cell(category_start_row, category_start_col + 1, "Average Health Score")
    health_by_category = (
        azure.groupby("lng_equipment_category")["asset_health_score"]
        .mean()
        .round(1)
        .sort_values(ascending=True)
    )
    for offset, (category, score) in enumerate(health_by_category.items(), start=1):
        ws.cell(category_start_row + offset, category_start_col, category)
        ws.cell(category_start_row + offset, category_start_col + 1, float(score))

    # Helper table 3: PHMSA incident count by year.
    year_start_row = 13
    year_start_col = 8
    ws.cell(year_start_row, year_start_col, "Year")
    ws.cell(year_start_row, year_start_col + 1, "Incident Count")
    if "year" in phmsa.columns and "incident_count" in phmsa.columns:
        year_summary = (
            phmsa.assign(year=phmsa["year"].astype(str))
            .groupby("year")["incident_count"]
            .sum()
            .sort_index()
        )
    else:
        year_summary = pd.Series(dtype=float)

    for offset, (year, count) in enumerate(year_summary.items(), start=1):
        ws.cell(year_start_row + offset, year_start_col, year)
        ws.cell(year_start_row + offset, year_start_col + 1, int(count))

    for row_number, col_start, col_end in [
        (priority_start_row, 1, 2),
        (category_start_row, category_start_col, category_start_col + 1),
        (year_start_row, year_start_col, year_start_col + 1),
    ]:
        for col_number in range(col_start, col_end + 1):
            cell = ws.cell(row_number, col_number)
            cell.fill = NAVY_FILL
            cell.font = WHITE_FONT

    style_range_as_grid(ws, priority_start_row, priority_start_row + len(priority_summary), 1, 2)
    style_range_as_grid(
        ws,
        category_start_row,
        category_start_row + len(health_by_category),
        category_start_col,
        category_start_col + 1,
    )
    style_range_as_grid(
        ws,
        year_start_row,
        year_start_row + len(year_summary),
        year_start_col,
        year_start_col + 1,
    )

    set_column_widths(ws)
    ws.freeze_panes = "A4"

    return {
        "total_assets": total_assets,
        "critical_assets": critical_assets,
        "high_priority_assets": high_priority_assets,
        "average_asset_health_score": average_health,
        "total_estimated_downtime_hours": total_downtime,
        "phmsa_incident_risk_records": phmsa_records,
        "metropt3_sample_records": metropt3_records,
        "priority_start_row": priority_start_row,
        "priority_row_count": len(priority_summary),
        "category_start_row": category_start_row,
        "category_row_count": len(health_by_category),
        "year_start_row": year_start_row,
        "year_row_count": len(year_summary),
    }


def create_dashboard_sheet(wb: Workbook, kpi_values: dict[str, object]) -> None:
    """Create a starter dashboard with KPI cards, chart placeholders, and charts."""
    ws = wb.create_sheet("Dashboard")
    apply_title(
        ws,
        "LNG Operations Technical Reliability Dashboard",
        "Portfolio demonstration using public industrial datasets adapted into LNG-style reliability categories.",
    )
    ws["A3"] = "Not ExxonMobil or PNG LNG operating data. Not a live plant dashboard."
    ws["A3"].font = Font(italic=True, color="9C0006")

    kpi_cards = [
        ("Total assets", kpi_values["total_assets"], GREEN_FILL),
        ("Critical assets", kpi_values["critical_assets"], RED_FILL),
        ("High priority assets", kpi_values["high_priority_assets"], AMBER_FILL),
        ("Average health score", kpi_values["average_asset_health_score"], BLUE_FILL),
        ("Total estimated downtime hours", kpi_values["total_estimated_downtime_hours"], BLUE_FILL),
        ("Incident risk records", kpi_values["phmsa_incident_risk_records"], BLUE_FILL),
        ("Compressor sample records", kpi_values["metropt3_sample_records"], BLUE_FILL),
    ]

    start_row = 5
    start_col = 1
    card_width = 3
    for index, (label, value, fill) in enumerate(kpi_cards):
        row_offset = 0 if index < 4 else 4
        col_offset = (index % 4) * card_width
        label_cell = ws.cell(start_row + row_offset, start_col + col_offset, label)
        value_cell = ws.cell(start_row + row_offset + 1, start_col + col_offset, value)

        for col_number in range(start_col + col_offset, start_col + col_offset + card_width):
            ws.cell(start_row + row_offset, col_number).fill = fill
            ws.cell(start_row + row_offset + 1, col_number).fill = fill
            ws.cell(start_row + row_offset, col_number).border = THIN_BORDER
            ws.cell(start_row + row_offset + 1, col_number).border = THIN_BORDER

        label_cell.font = BOLD_FONT
        value_cell.font = Font(size=14, bold=True)
        value_cell.number_format = "#,##0.0"

    guidance_start = 14
    ws.cell(guidance_start, 1, "Manual Excel Work Remaining")
    ws.cell(guidance_start, 2, "Guidance")
    ws.cell(guidance_start, 1).font = BOLD_FONT
    ws.cell(guidance_start, 2).font = BOLD_FONT
    guidance_rows = [
        ("Slicers", "Add slicers for LNG equipment category, maintenance priority, source dataset, and year."),
        ("Formatting", "Polish dashboard spacing, colors, and print layout after reviewing in Excel."),
        ("Charts", "Adjust chart labels, titles, and axis scales for final presentation."),
        ("Validation", "Review assumptions before sharing on GitHub, CV, or LinkedIn."),
    ]
    ws.append([])
    for offset, (area, action) in enumerate(guidance_rows, start=1):
        ws.cell(guidance_start + offset, 1, area)
        ws.cell(guidance_start + offset, 2, action)

    for row in ws.iter_rows(min_row=guidance_start, max_row=guidance_start + len(guidance_rows), min_col=1, max_col=2):
        for cell in row:
            cell.border = THIN_BORDER
            cell.alignment = Alignment(wrap_text=True, vertical="top")
    ws.cell(guidance_start, 1).fill = NAVY_FILL
    ws.cell(guidance_start, 1).font = WHITE_FONT
    ws.cell(guidance_start, 2).fill = NAVY_FILL
    ws.cell(guidance_start, 2).font = WHITE_FONT

    kpi_ws = wb["KPI_Calculations"]

    # Chart 1: maintenance priority count.
    if kpi_values["priority_row_count"] > 0:
        chart = BarChart()
        chart.title = "Maintenance Priority Count"
        chart.y_axis.title = "Assets"
        chart.x_axis.title = "Priority"
        start = int(kpi_values["priority_start_row"])
        end = start + int(kpi_values["priority_row_count"])
        data = Reference(kpi_ws, min_col=2, min_row=start, max_row=end)
        categories = Reference(kpi_ws, min_col=1, min_row=start + 1, max_row=end)
        chart.add_data(data, titles_from_data=True)
        chart.set_categories(categories)
        chart.height = 7
        chart.width = 12
        ws.add_chart(chart, "D14")

    # Chart 2: asset health by equipment category.
    if kpi_values["category_row_count"] > 0:
        chart = BarChart()
        chart.title = "Asset Health By LNG Equipment Category"
        chart.y_axis.title = "Health Score"
        chart.x_axis.title = "Equipment Category"
        start = int(kpi_values["category_start_row"])
        end = start + int(kpi_values["category_row_count"])
        data = Reference(kpi_ws, min_col=5, min_row=start, max_row=end)
        categories = Reference(kpi_ws, min_col=4, min_row=start + 1, max_row=end)
        chart.add_data(data, titles_from_data=True)
        chart.set_categories(categories)
        chart.height = 7
        chart.width = 14
        ws.add_chart(chart, "D29")

    # Chart 3: PHMSA incident count by year.
    if kpi_values["year_row_count"] > 0:
        chart = LineChart()
        chart.title = "PHMSA Incident Count By Year"
        chart.y_axis.title = "Incident Count"
        chart.x_axis.title = "Year"
        start = int(kpi_values["year_start_row"])
        end = start + int(kpi_values["year_row_count"])
        data = Reference(kpi_ws, min_col=9, min_row=start, max_row=end)
        categories = Reference(kpi_ws, min_col=8, min_row=start + 1, max_row=end)
        chart.add_data(data, titles_from_data=True)
        chart.set_categories(categories)
        chart.height = 7
        chart.width = 14
        ws.add_chart(chart, "L14")

    ws.column_dimensions["A"].width = 24
    ws.column_dimensions["B"].width = 70
    for col in range(3, 16):
        ws.column_dimensions[get_column_letter(col)].width = 14


def create_ai_recommendations_sheet(
    wb: Workbook, azure: pd.DataFrame, phmsa: pd.DataFrame
) -> None:
    """Create simple AI-style recommendations from available processed data."""
    ws = wb.create_sheet("AI_Recommendations")
    apply_title(
        ws,
        "AI Recommendations",
        "Starter recommendation table for portfolio discussion. Review by a qualified engineer would be required before real use.",
    )

    critical_count = int((azure["maintenance_priority"] == "Critical").sum())
    high_count = int((azure["maintenance_priority"] == "High").sum())
    incident_records = int(phmsa["incident_count"].sum()) if "incident_count" in phmsa.columns else len(phmsa)

    rows = [
        [
            "Asset reliability",
            f"{critical_count} assets are currently marked Critical.",
            "Review critical assets first and confirm the failure, error, and vibration drivers.",
            "Critical priority indicates repeated failures or poor public-data health score in the Azure reliability summary.",
        ],
        [
            "Maintenance planning",
            f"{high_count} assets are currently marked High priority.",
            "Plan inspection during the next maintenance window and review component replacement history.",
            "High priority assets may not require immediate shutdown, but they should not be ignored in a reliability review.",
        ],
        [
            "Incident risk awareness",
            f"PHMSA summary represents {incident_records} public incident records.",
            "Use PHMSA trends to discuss cause categories, consequence severity, and mechanical integrity context.",
            "PHMSA data supports risk awareness, not a formal integrity assessment for PNG LNG operations.",
        ],
        [
            "Compressor surveillance",
            "MetroPT-3 sample provides compressor pressure, oil temperature, current, and signal values.",
            "Monitor oil temperature, pressure trends, motor current, and operating-status signals.",
            "Public compressor trends demonstrate surveillance methods but are not LNG plant alarm limits.",
        ],
    ]

    ws.append([])
    header_row = ws.max_row + 1
    ws.append(["area", "finding", "recommendation", "engineering_rationale"])
    for row in rows:
        ws.append(row)

    for cell in ws[header_row]:
        cell.fill = NAVY_FILL
        cell.font = WHITE_FONT
    style_range_as_grid(ws, header_row, ws.max_row, 1, 4)
    set_column_widths(ws, max_width=55)
    ws.freeze_panes = f"A{header_row + 1}"


def create_assumptions_sheet(wb: Workbook) -> None:
    """Create the assumptions and limitations sheet."""
    ws = wb.create_sheet("Assumptions")
    apply_title(
        ws,
        "Assumptions",
        "Public datasets are adapted into LNG-style reliability categories for portfolio learning.",
    )

    rows = [
        (
            "Azure asset mapping",
            "Azure machine records are adapted into LNG-style asset categories.",
            "Use as a portfolio asset model, not a real facility register.",
        ),
        (
            "Operating-hour proxy",
            "Telemetry record count is used as an operating-hour proxy.",
            "MTBF-style values are approximate and should be labeled as estimates.",
        ),
        (
            "Downtime assumption",
            "Each failure is assumed to cause 8 downtime hours.",
            "Estimated downtime is a simple screening calculation.",
        ),
        (
            "Reliability KPIs",
            "MTBF-style and availability-style values are estimates for portfolio learning.",
            "Do not present as auditable plant reliability metrics.",
        ),
        (
            "MetroPT-3",
            "MetroPT-3 is a public compressor dataset adapted for LNG-style compressor surveillance.",
            "Trends are process-surveillance examples, not LNG alarm limits.",
        ),
        (
            "PHMSA",
            "PHMSA data is US public incident data used for risk-awareness context, not PNG LNG operating history.",
            "Use as incident awareness and mechanical integrity context only.",
        ),
        (
            "Assessment boundary",
            "This is not a formal mechanical integrity assessment or live plant dashboard.",
            "Workbook is a dashboard skeleton for GitHub, CV, and LinkedIn portfolio presentation.",
        ),
        (
            "Data confidentiality",
            "No ExxonMobil or PNG LNG operating data is used.",
            "All project claims must preserve this wording clearly.",
        ),
    ]

    ws.append([])
    header_row = ws.max_row + 1
    ws.append(["Assumption", "Description", "Dashboard implication"])
    for row in rows:
        ws.append(row)

    for cell in ws[header_row]:
        cell.fill = NAVY_FILL
        cell.font = WHITE_FONT
    style_range_as_grid(ws, header_row, ws.max_row, 1, 3)
    set_column_widths(ws, max_width=65)
    ws.freeze_panes = f"A{header_row + 1}"


def create_workbook(azure: pd.DataFrame, phmsa: pd.DataFrame, metropt3: pd.DataFrame) -> None:
    """Create and save the Excel dashboard skeleton workbook."""
    wb = Workbook()
    default_sheet = wb.active
    wb.remove(default_sheet)

    create_readme_sheet(wb)

    azure_ws = wb.create_sheet("Azure_Reliability_Summary")
    write_dataframe_sheet(azure_ws, azure, "tblAzureReliabilitySummary")

    phmsa_ws = wb.create_sheet("PHMSA_Incident_Risk")
    write_dataframe_sheet(phmsa_ws, phmsa, "tblPHMSAIncidentRisk")

    metro_ws = wb.create_sheet("MetroPT3_Compressor_Sample")
    write_dataframe_sheet(metro_ws, metropt3, "tblMetroPT3CompressorSample")

    kpi_values = create_kpi_calculations_sheet(wb, azure, phmsa, metropt3)
    create_dashboard_sheet(wb, kpi_values)
    create_ai_recommendations_sheet(wb, azure, phmsa)
    create_assumptions_sheet(wb)

    # Keep the requested order even if sheets were created in helper functions.
    requested_order = [
        "README",
        "Azure_Reliability_Summary",
        "PHMSA_Incident_Risk",
        "MetroPT3_Compressor_Sample",
        "KPI_Calculations",
        "Dashboard",
        "AI_Recommendations",
        "Assumptions",
    ]
    wb._sheets = [wb[sheet_name] for sheet_name in requested_order]

    WORKBOOK_OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    wb.save(WORKBOOK_OUTPUT_PATH)


def build_report(azure: pd.DataFrame, phmsa: pd.DataFrame, metropt3: pd.DataFrame) -> str:
    """Create the Excel dashboard build report."""
    return "\n".join(
        [
            "# Excel Dashboard Build Report",
            "",
            "## Workbook Created",
            "",
            f"- Workbook: `{WORKBOOK_OUTPUT_PATH.relative_to(PROJECT_ROOT).as_posix()}`",
            "- Status: starter/skeleton workbook, not final polished dashboard",
            "- Purpose: operations technical reliability dashboard portfolio demonstration",
            "",
            "## Datasets Feeding The Workbook",
            "",
            f"- `data/processed/azure_machine_reliability_summary.csv` ({len(azure):,} rows)",
            f"- `data/processed/phmsa_incident_risk_summary.csv` ({len(phmsa):,} grouped rows)",
            f"- `samples/metropt3/metropt3_compressor_sample.csv` ({len(metropt3):,} rows)",
            "",
            "These are public industrial datasets adapted into LNG-style reliability "
            "categories. They are not ExxonMobil or PNG LNG operating data.",
            "",
            "## Sheets Created",
            "",
            "- `README`",
            "- `Azure_Reliability_Summary`",
            "- `PHMSA_Incident_Risk`",
            "- `MetroPT3_Compressor_Sample`",
            "- `KPI_Calculations`",
            "- `Dashboard`",
            "- `AI_Recommendations`",
            "- `Assumptions`",
            "",
            "## KPIs Included",
            "",
            "- Total assets",
            "- Critical assets",
            "- High priority assets",
            "- Average asset health score",
            "- Total estimated downtime hours",
            "- PHMSA incident risk records",
            "- MetroPT-3 sample records",
            "",
            "## Charts Included",
            "",
            "- Maintenance priority count",
            "- Asset health by LNG equipment category",
            "- PHMSA incident count by year",
            "",
            "## Assumptions",
            "",
            "- Azure machines are mapped into LNG-style asset categories.",
            "- Telemetry record count is used as an operating-hour proxy.",
            "- Each failure is assumed to cause 8 downtime hours.",
            "- MTBF-style and availability-style values are estimates for portfolio learning.",
            "- MetroPT-3 is adapted for LNG-style compressor surveillance.",
            "- PHMSA is public US incident data used for risk-awareness context.",
            "- The workbook is not a formal mechanical integrity assessment or live plant dashboard.",
            "",
            "## Manual Excel Work Remaining",
            "",
            "- Review workbook visually in Excel and adjust chart placement if needed.",
            "- Add slicers for maintenance priority, LNG equipment category, source dataset, and year.",
            "- Polish dashboard formatting, chart labels, and print layout.",
            "- Add screenshots to `screenshots/` after the dashboard is visually acceptable.",
            "- Review all wording before GitHub, CV, or LinkedIn publication.",
            "",
            "## Portfolio Story Support",
            "",
            "This workbook connects Azure reliability scoring, MetroPT-3 compressor "
            "surveillance, and PHMSA incident risk awareness into one operations "
            "technical reliability dashboard. It demonstrates data preparation, "
            "reliability thinking, risk-awareness communication, and Excel-based "
            "presentation using public industrial datasets adapted into LNG-style "
            "reliability categories.",
            "",
        ]
    )


def main() -> None:
    """Run the workbook build workflow."""
    print("Building Excel dashboard skeleton...")
    print(f"Project root: {PROJECT_ROOT}")

    check_required_inputs()
    azure, phmsa, metropt3 = read_dashboard_inputs()

    create_workbook(azure, phmsa, metropt3)
    REPORT_OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    REPORT_OUTPUT_PATH.write_text(build_report(azure, phmsa, metropt3), encoding="utf-8")

    print()
    print("Excel dashboard skeleton build complete.")
    print(f"Workbook written: {WORKBOOK_OUTPUT_PATH.relative_to(PROJECT_ROOT)}")
    print(f"Build report written: {REPORT_OUTPUT_PATH.relative_to(PROJECT_ROOT)}")
    print(f"Azure rows loaded: {len(azure):,}")
    print(f"PHMSA grouped rows loaded: {len(phmsa):,}")
    print(f"MetroPT-3 sample rows loaded: {len(metropt3):,}")


if __name__ == "__main__":
    main()
