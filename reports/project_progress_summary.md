# Project Progress Summary

This report summarizes current progress on the LNG Operations Technical
Reliability Dashboard. The project uses public industrial datasets adapted into
LNG-style reliability categories for portfolio demonstration.

The project is not ExxonMobil or PNG LNG operating data. It does not contain
confidential, proprietary, or licensee data.

## Current Status

Status: v0.1 recruiter-review version complete.

The Version 0.1 dashboard skeleton has been visually polished, documented, and
pushed to GitHub for controlled recruiter review. The repository now contains
processed dashboard-ready data summaries, GitHub-safe samples, an Excel
dashboard workbook, updated screenshots, reproducible Python scripts, and
public-facing documentation.

The workbook is available at:

`excel/lng_operations_reliability_dashboard.xlsx`

Screenshots are available in:

`screenshots/`

## Completed So Far

- Repository structure created for `docs/`, `data/`, `reports/`, `samples/`,
  `scripts/`, `excel/`, `notebooks/`, and supporting folders.
- Raw public datasets downloaded locally under `data/raw/`.
- Raw public datasets excluded from GitHub.
- `.gitignore` configured to keep raw ZIP, raw CSV, raw text, raw Excel, and
  extracted raw files out of Git.
- Azure Predictive Maintenance dataset inspected.
- Azure machine reliability summary built with LNG-style equipment categories,
  asset health score, maintenance priority, MTBF-style hours, MTTR-style hours,
  and availability-style percent.
- MetroPT-3 Compressor dataset inspected and documented for compressor process
  surveillance.
- MetroPT-3 compressor sample and profile created.
- PHMSA LNG and Gas Transmission incident datasets inspected.
- PHMSA incident risk-awareness summary created for dashboard use.
- Public datasets processed into dashboard-ready files under `data/processed/`.
- GitHub-safe sample files created under `samples/`.
- Data profile and summary reports created under `reports/`.
- Excel dashboard workbook created and visually polished under `excel/`.
- Dashboard screenshots updated under `screenshots/`.
- README updated with screenshots, review path, limitations, and workbook link.
- GitHub repository pushed for portfolio review.

## Public Datasets Downloaded, Inspected, And Processed

| Dataset | Local Raw/Extracted Location | Current Status |
|---|---|---|
| Azure Predictive Maintenance | `data/raw/extracted/azure_pdm/` | Inspected and processed into `data/processed/azure_machine_reliability_summary.csv` |
| MetroPT-3 Compressor | `data/raw/extracted/metropt3/` | Inspected, documented, and sampled into `samples/metropt3/metropt3_compressor_sample.csv` |
| PHMSA LNG Incidents | `data/raw/extracted/phmsa_lng/` | Inspected and sampled into `samples/phmsa/phmsa_lng_incident_sample.csv` |
| PHMSA Gas Transmission Incidents | `data/raw/extracted/phmsa_gas_transmission/` | Inspected, sampled, and processed into `data/processed/phmsa_incident_risk_summary.csv` |

## Scripts Created

| Script | Purpose |
|---|---|
| `scripts/inspect_azure_pdm.py` | Profiles Azure PdM raw files and creates report/sample outputs |
| `scripts/build_azure_reliability_summary.py` | Builds `data/processed/azure_machine_reliability_summary.csv` |
| `scripts/inspect_metropt3_compressor.py` | Profiles MetroPT-3 compressor data and creates report/sample outputs |
| `scripts/inspect_phmsa_incidents.py` | Profiles PHMSA LNG and Gas Transmission data, creates samples, and builds incident risk summary |
| `scripts/build_excel_dashboard_skeleton.py` | Builds `excel/lng_operations_reliability_dashboard.xlsx` |

## Dashboard-Ready Processed Files

| File | Dashboard Use |
|---|---|
| `data/processed/azure_machine_reliability_summary.csv` | Asset reliability, health score, maintenance priority, and downtime-style KPIs |
| `data/processed/phmsa_incident_risk_summary.csv` | LNG and pipeline incident risk-awareness summary |

## GitHub-Safe Sample Files

| Folder | Contents |
|---|---|
| `samples/azure/` | Azure source samples and machine reliability summary sample |
| `samples/metropt3/` | MetroPT-3 compressor sample capped at 1,000 rows |
| `samples/phmsa/` | PHMSA LNG and Gas Transmission incident samples capped where applicable |

## Excel Workbook And Screenshots

| Artifact | Purpose |
|---|---|
| `excel/lng_operations_reliability_dashboard.xlsx` | Excel dashboard skeleton with data sheets, KPI calculations, dashboard, AI recommendations, and assumptions |
| `screenshots/dashboard_preview.png` | Quick view of the main dashboard sheet |
| `screenshots/kpi_calculations.png` | Quick view of the KPI calculations sheet |
| `screenshots/ai_recommendations.png` | Quick view of the AI recommendations starter table |

## Reports Created

| Report | Purpose |
|---|---|
| `reports/azure_data_profile.md` | Azure source data profile |
| `reports/azure_reliability_summary_report.md` | Azure reliability summary explanation |
| `reports/metropt3_data_profile.md` | MetroPT-3 compressor data profile |
| `reports/metropt3_compressor_surveillance_plan.md` | MetroPT-3 compressor dashboard planning |
| `reports/phmsa_incident_data_profile.md` | PHMSA source data profile |
| `reports/phmsa_incident_risk_summary_report.md` | PHMSA risk-awareness summary explanation |
| `reports/excel_dashboard_build_report.md` | Excel workbook build summary |
| `reports/project_progress_summary.md` | Current project status and next steps |
| `reports/version_1_release_notes.md` | Version 0.1 release notes |
| `reports/repo_quality_review.md` | Repository quality review |
| `reports/recruiter_review_notes.md` | Recruiter/reviewer navigation guide |

## Future v0.2 Improvements

The v0.1 recruiter-review version is complete. Future v0.2 improvements may
include:

1. Add Excel slicers for maintenance priority, LNG equipment category, source
   dataset, and year.
2. Add additional compressor trend charts for pressure, oil temperature, motor
   current, and operating signals.
3. Add workbook QA checks for sheet presence, missing references, row heights,
   and key formatting expectations.
4. Create a more compact executive summary for quick recruiter scanning.
5. Continue confirming that raw datasets remain excluded from GitHub.

## Honest CV / LinkedIn Project Description

Built an operations technical reliability dashboard using Python, pandas, and
Excel with public industrial datasets adapted into LNG-style reliability
categories. Processed Azure Predictive Maintenance data into asset health and
maintenance-priority summaries, profiled MetroPT-3 compressor data for
process-surveillance trends, and summarized public PHMSA LNG and Gas
Transmission incident data for risk awareness. Created a visually polished Excel
dashboard workbook and screenshots for portfolio review. This is a portfolio
demonstration and is not ExxonMobil or PNG LNG operating data.

## Current Positioning

The project is ready for controlled recruiter review as the completed Version
0.1 recruiter-review dashboard. The repo demonstrates public-data handling,
reliability thinking, Excel dashboard communication, and transparent
assumptions. It should be presented as a portfolio demonstration, not as a live
plant dashboard or formal mechanical integrity assessment.
