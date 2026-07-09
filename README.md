# LNG Operations Technical Reliability Dashboard

[![Python 3.11](https://img.shields.io/badge/python-3.11-blue.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

## Important Disclaimer

This project uses **public industrial datasets** adapted into LNG-style
reliability categories for **portfolio demonstration**.

It does **not** contain, use, or claim to use ExxonMobil or PNG LNG operating
data. It does **not** contain confidential, proprietary, or licensee data. It is
not affiliated with or endorsed by ExxonMobil, PNG LNG, or any LNG operator.

This is an **operations technical reliability dashboard** starter project. It is
not a live plant dashboard, not an industrial digital twin, and not a formal
mechanical integrity assessment.

## Project Objective

Build a clear, honest, GitHub-ready reliability dashboard that demonstrates how
a graduate Mechanical Engineer can use Python and Excel to inspect public
industrial datasets, adapt them into LNG-style reliability categories, and
communicate operations technical insights.

The project focuses on:

- Asset reliability and maintenance priority
- Compressor process surveillance
- LNG and pipeline incident risk awareness
- Mechanical integrity context
- Excel dashboard communication for non-Python reviewers

## Why This Project Matters

LNG Operations Technical support requires engineers to understand equipment
health, rotating equipment behavior, incident trends, maintenance priorities,
and risk communication. Real plant data is confidential, so this project uses
public datasets to demonstrate the workflow without misrepresenting the source
of the data.

The value is in the engineering method:

- Inspect and document data sources
- Create small GitHub-safe samples
- Build processed dashboard-ready tables
- Calculate transparent reliability-style indicators
- State assumptions and limitations clearly
- Present results in an Excel workbook suitable for portfolio review

## Public Datasets Used

| Dataset | Public Source | Used For |
|---|---|---|
| Microsoft Azure Predictive Maintenance Dataset | Microsoft / Kaggle public dataset | Asset reliability summary, maintenance priority, health score, MTBF-style and availability-style estimates |
| MetroPT-3 Compressor Dataset | Public compressor dataset from UCI / associated publication | Compressor process surveillance sample, oil temperature, pressure, motor current, and operating signals |
| PHMSA LNG and Gas Transmission Incident Data | U.S. DOT Pipeline and Hazardous Materials Safety Administration | LNG incident awareness, pipeline incident trends, cause categories, consequence context |

See [docs/data_sources.md](docs/data_sources.md) for source details and
attribution.

## Current Features

- Azure Predictive Maintenance data inspection script
- Azure dashboard-ready machine reliability summary
- MetroPT-3 compressor data inspection script
- MetroPT-3 compressor surveillance planning report
- PHMSA LNG and Gas Transmission incident inspection script
- PHMSA dashboard-ready incident risk-awareness summary
- GitHub-safe sample files for Azure, MetroPT-3, and PHMSA
- Excel dashboard skeleton at
  [excel/lng_operations_reliability_dashboard.xlsx](excel/lng_operations_reliability_dashboard.xlsx)
- Documentation for dashboard data model and Excel design
- Release notes, progress summary, and dashboard review checklist

## Repository Structure

```text
.
|-- data/
|   |-- raw/                 # Local raw public datasets, ignored by Git
|   |-- processed/           # Dashboard-ready processed CSV files
|   `-- README.md
|-- docs/                    # Project design, data model, and presentation docs
|-- excel/                   # Excel dashboard workbook
|-- notebooks/               # Reserved for future notebook workflow
|-- reports/                 # Generated reports and review documents
|-- samples/                 # Small GitHub-safe sample files
|-- screenshots/             # Dashboard screenshots to add later
|-- scripts/                 # Reproducible Python scripts
|-- src/                     # Reserved for reusable Python modules
|-- README.md
|-- requirements.txt
`-- LICENSE
```

## How To Run Scripts

From Windows CMD:

```cmd
cd /d D:\ai-portfolio-projects\lng-reliability-dashboard
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

Run the project scripts:

```cmd
python scripts\inspect_azure_pdm.py
python scripts\build_azure_reliability_summary.py
python scripts\inspect_metropt3_compressor.py
python scripts\inspect_phmsa_incidents.py
python scripts\build_excel_dashboard_skeleton.py
```

The scripts read from processed/sample files or local raw files under
`data/raw/`. Raw files are not committed to Git.

## How To Open The Excel Workbook

Open this file in Microsoft Excel:

```text
excel/lng_operations_reliability_dashboard.xlsx
```

The workbook currently includes these sheets:

- `README`
- `Azure_Reliability_Summary`
- `PHMSA_Incident_Risk`
- `MetroPT3_Compressor_Sample`
- `KPI_Calculations`
- `Dashboard`
- `AI_Recommendations`
- `Assumptions`

The workbook is a dashboard skeleton. It includes KPI cards, starter charts,
data tables, assumptions, and guidance for manual Excel polish.

## Current Project Status

Current release: `v0.1-dashboard-skeleton`

Completed:

- Public datasets downloaded locally and inspected
- Raw files excluded from Git
- Processed Azure reliability summary created
- Processed PHMSA incident risk summary created
- MetroPT-3 compressor sample created
- Excel dashboard skeleton created
- GitHub/CV/LinkedIn presentation docs created

Remaining before final Version 1 presentation:

- Open and visually review the Excel workbook
- Adjust dashboard chart placement and formatting manually if needed
- Add slicers in Excel
- Capture screenshots into `screenshots/`
- Add screenshots to this README
- Run all scripts from a clean terminal before final release

## Skills Demonstrated

- Python scripting for engineering data workflows
- `pandas` data cleaning, grouping, and summarization
- Excel workbook generation with `openpyxl`
- Reliability-style KPI calculation
- Maintenance priority ranking
- Compressor process-surveillance thinking
- PHMSA incident risk-awareness analysis
- Dashboard data modeling
- Technical documentation for GitHub and portfolio review
- Clear data provenance and assumption management

## Limitations

- Public datasets are adapted into LNG-style reliability categories.
- This is not ExxonMobil or PNG LNG operating data.
- This is not a live plant dashboard.
- This is not a formal mechanical integrity assessment.
- Azure MTBF-style, MTTR-style, and availability-style values are estimates for
  learning and presentation.
- MetroPT-3 is a public compressor dataset, not LNG plant compressor history.
- PHMSA data is U.S. public incident data, not PNG LNG operating history.
- The Excel workbook is a starter dashboard skeleton, not a final production
  dashboard.

See [docs/assumptions_and_limitations.md](docs/assumptions_and_limitations.md)
for the full honesty document.

## Suggested Screenshots

Screenshots will be added after the workbook is visually reviewed. Planned
screenshots:

- Dashboard overview
- Azure asset health by equipment category
- Maintenance priority count
- PHMSA incident trends
- MetroPT-3 compressor trend
- Assumptions sheet

## Next Steps

1. Review `excel/lng_operations_reliability_dashboard.xlsx` manually in Excel.
2. Add slicers and polish chart placement.
3. Capture dashboard screenshots.
4. Add screenshots to the README.
5. Commit documentation, processed files, sample files, scripts, reports, and the
   workbook.
6. Push to GitHub.
7. Add a concise project description to CV and LinkedIn.

## Contact / Portfolio Note

This repository is intended as a mechanical engineering portfolio project for
LNG Operations Technical, reliability, and maintenance engineering roles. The
project demonstrates initiative, data analysis, reliability thinking, and honest
technical communication using public industrial datasets.

## License

MIT - see [LICENSE](LICENSE).
