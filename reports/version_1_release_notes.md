# Version 1 Release Notes

## Version Name

`v0.1-dashboard-skeleton`

## Release Summary

This release creates the first complete dashboard skeleton for the LNG
Operations Technical Reliability Dashboard. It connects processed Azure
Predictive Maintenance data, MetroPT-3 compressor sample data, and public PHMSA
incident data into an Excel workbook and supporting documentation.

This is a portfolio demonstration using public industrial datasets adapted into
LNG-style reliability categories. It is not ExxonMobil or PNG LNG operating
data, not a live plant dashboard, and not a formal mechanical integrity
assessment.

## What Is Included

- Azure Predictive Maintenance data profile
- Azure machine reliability summary
- MetroPT-3 compressor data profile
- MetroPT-3 compressor surveillance plan
- PHMSA LNG and Gas Transmission incident data profile
- PHMSA incident risk-awareness summary
- Excel dashboard skeleton
- Dashboard data model documentation
- Excel dashboard design documentation
- GitHub, CV, and LinkedIn presentation guidance
- GitHub-safe sample files
- Project progress summary and review checklist

## Public Datasets Used

| Dataset | Use In This Release |
|---|---|
| Microsoft Azure Predictive Maintenance Dataset | Asset reliability, health score, maintenance priority, MTBF-style and availability-style estimates |
| MetroPT-3 Compressor Dataset | Compressor process-surveillance sample and trend planning |
| PHMSA LNG Incident Data | LNG incident awareness and consequence context |
| PHMSA Gas Transmission Incident Data | Pipeline incident trends, cause category review, and mechanical integrity context |

## Files Created

Key scripts:

- `scripts/inspect_azure_pdm.py`
- `scripts/build_azure_reliability_summary.py`
- `scripts/inspect_metropt3_compressor.py`
- `scripts/inspect_phmsa_incidents.py`
- `scripts/build_excel_dashboard_skeleton.py`

Key processed files:

- `data/processed/azure_machine_reliability_summary.csv`
- `data/processed/phmsa_incident_risk_summary.csv`

Key workbook:

- `excel/lng_operations_reliability_dashboard.xlsx`

Key documentation and reports:

- `docs/dashboard_data_model.md`
- `docs/excel_dashboard_design.md`
- `docs/github_portfolio_presentation.md`
- `reports/project_progress_summary.md`
- `reports/excel_dashboard_build_report.md`
- `reports/dashboard_review_checklist.md`
- `reports/version_1_release_notes.md`

Sample folders:

- `samples/azure/`
- `samples/metropt3/`
- `samples/phmsa/`

## Known Limitations

- The workbook is a dashboard starter/skeleton, not a final polished dashboard.
- No real-time plant data connection exists.
- No CMMS, historian, SAP PM, PI System, or live operations system is connected.
- Azure machines are public machine records mapped into LNG-style categories.
- MetroPT-3 is a public compressor dataset, not an LNG refrigerant compressor
  dataset.
- PHMSA data is US public incident data, not PNG LNG operating history.
- MTBF-style, MTTR-style, and availability-style metrics are estimates for
  portfolio learning.
- PHMSA output is a risk-awareness summary, not a formal integrity assessment.
- Manual Excel polish and screenshots remain before public portfolio release.

## What Remains For v0.2

- Manually review and polish the Excel dashboard layout.
- Add slicers for maintenance priority, LNG equipment category, source dataset,
  and year.
- Add or refine charts for compressor oil temperature and pressure trends.
- Capture screenshots and add them to `screenshots/`.
- Add screenshots to README.
- Consider a small automated workbook QA script.
- Add optional chart export workflow for portfolio images.
- Refine AI recommendation wording after reviewing dashboard results.
- Run all scripts from a clean environment and document the exact workflow.

## Confidentiality Statement

No ExxonMobil or PNG LNG confidential data is used in this release. No
ExxonMobil or PNG LNG operating data is used. All data sources are public
industrial datasets adapted into LNG-style reliability categories for portfolio
demonstration.
