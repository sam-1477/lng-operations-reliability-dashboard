# Recruiter Review Notes

This guide explains how a recruiter or engineering reviewer can navigate the LNG
Operations Technical Reliability Dashboard quickly.

## Recommended Review Path

### 1. Start With `README.md`

Open the README first. It explains:

- Project purpose
- Public industrial datasets used
- Dashboard screenshots
- Excel workbook location
- Scripts created
- Current status
- Limitations
- Clear disclaimer that this is not ExxonMobil or PNG LNG operating data

The README is the best first-pass view for a recruiter.

### 2. View Dashboard Screenshots

The README embeds the main screenshots:

- `screenshots/dashboard_preview.png`
- `screenshots/kpi_calculations.png`
- `screenshots/ai_recommendations.png`

These screenshots show the current Excel dashboard skeleton and help a reviewer
understand the project visually before opening any files.

### 3. Open The Excel Workbook

Open:

`excel/lng_operations_reliability_dashboard.xlsx`

Recommended sheets to inspect:

- `README` for workbook purpose and data-source notes
- `Dashboard` for KPI cards and starter charts
- `KPI_Calculations` for summary metrics
- `Azure_Reliability_Summary` for asset reliability rows
- `PHMSA_Incident_Risk` for incident risk-awareness rows
- `MetroPT3_Compressor_Sample` for compressor surveillance sample data
- `Assumptions` for limitations and public-data caveats

The workbook is a dashboard skeleton, not a final production dashboard.

### 4. Review Project Progress

Open:

`reports/project_progress_summary.md`

This report explains what has been completed, which public datasets were
downloaded and inspected, which scripts were created, and which processed files
feed the dashboard.

### 5. Review Release Notes

Open:

`reports/version_1_release_notes.md`

This report explains the current release, `v0.1-dashboard-skeleton`, including
what is included, known limitations, and what remains for the next version.

### 6. Review Data Source Documentation

Open:

`docs/data_sources.md`

Then, if more detail is needed, review:

- `docs/dashboard_data_model.md`
- `docs/excel_dashboard_design.md`
- `docs/assumptions_and_limitations.md`
- `samples/README.md`

These files explain how the public datasets are used and how they are adapted
into LNG-style reliability categories.

### 7. Understand Limitations

The most important limitations are:

- This project uses public industrial datasets.
- The datasets are adapted into LNG-style reliability categories.
- This is a portfolio demonstration.
- This is not ExxonMobil or PNG LNG operating data.
- This is not a live plant dashboard.
- This is not a formal mechanical integrity assessment.
- Reliability-style values are learning estimates, not audited plant KPIs.

These limitations are a strength of the project because they show professional
data ethics and clear engineering communication.

## What To Look For As A Reviewer

- Does the candidate communicate assumptions clearly?
- Does the candidate avoid overclaiming?
- Does the candidate understand reliability and maintenance concepts?
- Does the candidate show practical Python and Excel capability?
- Does the candidate organize public data into a usable dashboard structure?
- Does the candidate connect compressor surveillance, incident awareness, and
  maintenance priority to LNG Operations Technical work?

## Quick Reviewer Summary

This repository is a credible graduate Mechanical Engineering portfolio project.
It is most useful as evidence of initiative, reliability thinking, Python/Excel
workflow, public data handling, and honest technical communication. It should be
reviewed as a portfolio demonstration, not as a real LNG plant analysis.
