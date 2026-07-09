# Dashboard Review Checklist

Use this checklist before presenting the LNG Operations Technical Reliability
Dashboard on GitHub, CV, LinkedIn, or in an interview.

## Workbook Opening Check

- [ ] `excel/lng_operations_reliability_dashboard.xlsx` opens without repair
      warnings.
- [ ] Workbook opens to a sensible first sheet.
- [ ] File size is reasonable for GitHub.
- [ ] No links to local raw data files are required to open the workbook.
- [ ] Workbook is clearly labeled as a dashboard skeleton / portfolio
      demonstration.

## Sheet Presence Check

Confirm these sheets exist:

- [ ] `README`
- [ ] `Azure_Reliability_Summary`
- [ ] `PHMSA_Incident_Risk`
- [ ] `MetroPT3_Compressor_Sample`
- [ ] `KPI_Calculations`
- [ ] `Dashboard`
- [ ] `AI_Recommendations`
- [ ] `Assumptions`

## Data Source Check

- [ ] README sheet lists Microsoft Azure Predictive Maintenance.
- [ ] README sheet lists MetroPT-3 Compressor Dataset.
- [ ] README sheet lists PHMSA LNG/Gas Transmission Incident Data.
- [ ] Data sheets load from processed or sample files only.
- [ ] No raw ZIP, raw CSV, raw TXT, raw Excel, or extracted raw files are
      included in Git.
- [ ] `git status --short data\raw` shows no staged or unstaged raw-data
      changes.

## KPI Check

- [ ] Total assets matches the Azure reliability summary row count.
- [ ] Critical assets count matches `maintenance_priority = Critical`.
- [ ] High priority assets count matches `maintenance_priority = High`.
- [ ] Average health score is visibly labeled as a screening metric.
- [ ] Total estimated downtime hours is based on the documented 8-hour
      assumption per failure.
- [ ] PHMSA incident risk records match the grouped incident count total.
- [ ] MetroPT-3 sample records match the sample row count.

## Dashboard Visual Check

- [ ] KPI cards are readable.
- [ ] Maintenance priority chart is visible and understandable.
- [ ] Asset health by LNG equipment category chart is visible and understandable.
- [ ] PHMSA incident count by year chart is visible and understandable.
- [ ] Chart titles and axis labels do not overclaim real plant performance.
- [ ] Dashboard note says this is not ExxonMobil or PNG LNG operating data.
- [ ] Dashboard note says this is not a live plant dashboard.

## Honesty / Claims Check

- [ ] README contains the phrase `public industrial datasets`.
- [ ] README contains the phrase `adapted into LNG-style reliability categories`.
- [ ] README contains the phrase `portfolio demonstration`.
- [ ] README contains the phrase `not ExxonMobil or PNG LNG operating data`.
- [ ] README contains the phrase `not a live plant dashboard`.
- [ ] README contains the phrase `not a formal mechanical integrity assessment`.
- [ ] No file claims that the project uses real PNG LNG operating data.
- [ ] No file claims that the project is affiliated with or endorsed by
      ExxonMobil or PNG LNG.
- [ ] No file claims that this is an industrial digital twin.
- [ ] No file claims production deployment or real-time monitoring.

## GitHub Readiness Check

- [ ] README is clear for a first-time visitor.
- [ ] README explains how to run scripts.
- [ ] README explains how to open the Excel workbook.
- [ ] `docs/dashboard_data_model.md` exists.
- [ ] `docs/excel_dashboard_design.md` exists.
- [ ] `docs/github_portfolio_presentation.md` exists.
- [ ] `reports/project_progress_summary.md` exists.
- [ ] `reports/version_1_release_notes.md` exists.
- [ ] Screenshots are added or the README clearly says screenshots are pending.
- [ ] `.gitignore` excludes raw data.

## CV Readiness Check

- [ ] CV wording says personal portfolio project.
- [ ] CV wording says public industrial datasets.
- [ ] CV wording says adapted into LNG-style reliability categories.
- [ ] CV wording does not say real LNG plant data.
- [ ] CV wording does not imply employment or access to confidential data.
- [ ] CV wording emphasizes skills: Python, Excel, reliability, maintenance,
      compressor surveillance, PHMSA risk awareness.

## LinkedIn Readiness Check

- [ ] Post wording is honest and concise.
- [ ] Post says this is a portfolio demonstration.
- [ ] Post says no ExxonMobil or PNG LNG operating data is used.
- [ ] Post avoids tagging official company accounts unless appropriate.
- [ ] Post avoids using company logos or proprietary branding.
- [ ] GitHub link works before posting.

## Remaining Improvements Before Version 1 Is Complete

- [ ] Open the Excel workbook manually and adjust chart placement if needed.
- [ ] Add dashboard screenshots under `screenshots/`.
- [ ] Add screenshot images to README after screenshots are captured.
- [ ] Run every script from a clean Windows CMD session.
- [ ] Review all reports for consistent public-data wording.
- [ ] Confirm `git status --short` does not show raw data.
- [ ] Commit scripts, docs, reports, processed files, samples, and workbook.
- [ ] Push to GitHub.
- [ ] Add the project to CV and LinkedIn only after the GitHub repo is readable.
