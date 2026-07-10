# Reviewer Quick Start

This guide gives recruiters and engineering reviewers a short path through the
LNG Operations Technical Reliability Dashboard repository.

The project uses public industrial datasets adapted into LNG-style reliability
categories for portfolio demonstration. It is not ExxonMobil or PNG LNG
operating data, not a live plant dashboard, and not a formal mechanical
integrity assessment.

## Recommended Review Path

1. Read [README.md](../README.md)
   - Start here for the project purpose, dashboard screenshots, public datasets,
     limitations, and current status.

2. View the dashboard screenshots
   - [Dashboard preview](../screenshots/dashboard_preview.png)
   - [KPI calculations](../screenshots/kpi_calculations.png)
   - [AI recommendations](../screenshots/ai_recommendations.png)

3. Open the Excel workbook
   - [excel/lng_operations_reliability_dashboard.xlsx](../excel/lng_operations_reliability_dashboard.xlsx)
   - Review the `README`, `Dashboard`, `KPI_Calculations`,
     `Azure_Reliability_Summary`, `PHMSA_Incident_Risk`,
     `MetroPT3_Compressor_Sample`, `AI_Recommendations`, and `Assumptions`
     sheets.

4. Review the project progress summary
   - [reports/project_progress_summary.md](../reports/project_progress_summary.md)
   - Use this to understand what has been completed and what remains.

5. Review Version 0.1 release notes
   - [reports/version_1_release_notes.md](../reports/version_1_release_notes.md)
   - Use this to understand the current release scope and limitations.

6. Check data sources and assumptions
   - [docs/data_sources.md](data_sources.md)
   - [docs/assumptions_and_limitations.md](assumptions_and_limitations.md)
   - These explain where the public datasets came from and how they are adapted
     for portfolio use.

## What To Look For

- Clear explanation of public industrial datasets.
- Honest wording that the data is adapted into LNG-style reliability categories.
- Dashboard-ready processed files in `data/processed/`.
- GitHub-safe samples in `samples/`.
- Excel workbook in `excel/`.
- Screenshots in `screenshots/`.
- Clear limitations and no claim of ExxonMobil or PNG LNG operating data.

## Suggested Review Time

- 2 minutes: README and screenshots.
- 5 minutes: Excel workbook dashboard and assumptions.
- 10 minutes: project progress, release notes, data sources, and limitations.
