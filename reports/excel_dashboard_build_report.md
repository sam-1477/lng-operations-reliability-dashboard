# Excel Dashboard Build Report

## Workbook Created

- Workbook: `excel/lng_operations_reliability_dashboard.xlsx`
- Status: starter/skeleton workbook, not final polished dashboard
- Purpose: operations technical reliability dashboard portfolio demonstration

## Datasets Feeding The Workbook

- `data/processed/azure_machine_reliability_summary.csv` (100 rows)
- `data/processed/phmsa_incident_risk_summary.csv` (1,564 grouped rows)
- `samples/metropt3/metropt3_compressor_sample.csv` (1,000 rows)

These are public industrial datasets adapted into LNG-style reliability categories. They are not ExxonMobil or PNG LNG operating data.

## Sheets Created

- `README`
- `Azure_Reliability_Summary`
- `PHMSA_Incident_Risk`
- `MetroPT3_Compressor_Sample`
- `KPI_Calculations`
- `Dashboard`
- `AI_Recommendations`
- `Assumptions`

## KPIs Included

- Total assets
- Critical assets
- High priority assets
- Average asset health score
- Total estimated downtime hours
- PHMSA incident risk records
- MetroPT-3 sample records

## Charts Included

- Maintenance priority count
- Asset health by LNG equipment category
- PHMSA incident count by year

## Assumptions

- Azure machines are mapped into LNG-style asset categories.
- Telemetry record count is used as an operating-hour proxy.
- Each failure is assumed to cause 8 downtime hours.
- MTBF-style and availability-style values are estimates for portfolio learning.
- MetroPT-3 is adapted for LNG-style compressor surveillance.
- PHMSA is public US incident data used for risk-awareness context.
- The workbook is not a formal mechanical integrity assessment or live plant dashboard.

## Manual Excel Work Remaining

- Review workbook visually in Excel and adjust chart placement if needed.
- Add slicers for maintenance priority, LNG equipment category, source dataset, and year.
- Polish dashboard formatting, chart labels, and print layout.
- Add screenshots to `screenshots/` after the dashboard is visually acceptable.
- Review all wording before GitHub, CV, or LinkedIn publication.

## Portfolio Story Support

This workbook connects Azure reliability scoring, MetroPT-3 compressor surveillance, and PHMSA incident risk awareness into one operations technical reliability dashboard. It demonstrates data preparation, reliability thinking, risk-awareness communication, and Excel-based presentation using public industrial datasets adapted into LNG-style reliability categories.
