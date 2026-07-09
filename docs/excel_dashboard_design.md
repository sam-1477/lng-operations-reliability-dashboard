# Excel Dashboard Design

This document defines the first Excel workbook design for the LNG Operations
Technical Reliability Dashboard. The workbook should be clear enough for a
non-Python reviewer to understand the data, calculations, assumptions, and
dashboard outputs.

The workbook is a portfolio demonstration built from public industrial datasets
adapted into LNG-style reliability categories. It is not ExxonMobil or PNG LNG
operating data, and it is not a live plant dashboard.

## Recommended Workbook

`excel/lng_operations_reliability_dashboard.xlsx`

## Recommended Sheets

| Sheet | Purpose |
|---|---|
| `README` | Workbook purpose, data sources, refresh steps, and honesty statement |
| `Azure_Reliability_Summary` | Imported `data/processed/azure_machine_reliability_summary.csv` |
| `PHMSA_Incident_Risk` | Imported `data/processed/phmsa_incident_risk_summary.csv` |
| `MetroPT3_Compressor_Sample` | Imported `samples/metropt3/metropt3_compressor_sample.csv` |
| `KPI_Calculations` | Formula cells, Pivot Tables, helper tables, and dashboard-ready summaries |
| `Dashboard` | Main visual dashboard and KPI cards |
| `AI_Recommendations` | Optional engineering recommendations with clear review caveat |
| `Assumptions` | Public-data assumptions, limitations, and wording caveats |

## Recommended Excel Tables

| Sheet | Excel Table Name |
|---|---|
| `Azure_Reliability_Summary` | `tblAzureReliabilitySummary` |
| `PHMSA_Incident_Risk` | `tblPHMSAIncidentRisk` |
| `MetroPT3_Compressor_Sample` | `tblMetroPT3CompressorSample` |
| `KPI_Calculations` | `tblKpiSummary` |
| `Assumptions` | `tblAssumptions` |

## Dashboard Layout

Use one main `Dashboard` sheet with a simple operations-technical layout:

1. Header band
   - Title: `LNG Operations Technical Reliability Dashboard`
   - Subtitle: `Public industrial datasets adapted into LNG-style reliability categories`
   - Note: `Portfolio demonstration - not ExxonMobil or PNG LNG operating data`

2. KPI card row
   - Total assets
   - Critical assets
   - High priority assets
   - Average health score
   - Total estimated downtime hours
   - Incident risk records
   - Compressor sample records

3. Asset reliability section
   - Asset health by LNG equipment category
   - Maintenance priority count
   - Failure count by asset
   - Average vibration by equipment category

4. Incident risk section
   - PHMSA incident count by year
   - PHMSA incident count by cause category if available
   - PHMSA incident records by source dataset
   - Consequence severity summary using cost, fatalities, and injuries where available

5. Compressor surveillance section
   - Compressor oil temperature trend if `timestamp` exists
   - Compressor pressure trend using available pressure columns
   - Motor current trend if space allows

6. Assumptions footer
   - Short note pointing to the `Assumptions` sheet
   - Clear wording that outputs are estimates or screening summaries

## KPI Cards

Recommended KPI formulas assume the source ranges have been converted to Excel
Tables with the names listed above.

| KPI Card | Example Formula |
|---|---|
| Total assets | `=ROWS(tblAzureReliabilitySummary[machineID])` |
| Critical assets | `=COUNTIF(tblAzureReliabilitySummary[maintenance_priority],"Critical")` |
| High priority assets | `=COUNTIF(tblAzureReliabilitySummary[maintenance_priority],"High")` |
| Average health score | `=ROUND(AVERAGE(tblAzureReliabilitySummary[asset_health_score]),1)` |
| Total estimated downtime hours | `=SUM(tblAzureReliabilitySummary[estimated_downtime_hours])` |
| Incident risk records | `=SUM(tblPHMSAIncidentRisk[incident_count])` |
| Compressor sample records | `=ROWS(tblMetroPT3CompressorSample[timestamp])` |

Formatting guidance:

- Use large numbers for KPI values.
- Use red/amber/green conditional formatting for priority and health score.
- Label estimates clearly, for example `Availability-style %` and
  `MTBF-style hours`.

## Suggested Charts

| Chart | Source Table | Suggested Chart Type |
|---|---|---|
| Asset health by LNG equipment category | `tblAzureReliabilitySummary` | Clustered column or bar chart |
| Maintenance priority count | `tblAzureReliabilitySummary` | Donut or bar chart |
| Failure count by asset | `tblAzureReliabilitySummary` | Horizontal bar chart, top 10 assets |
| Average vibration by equipment category | `tblAzureReliabilitySummary` | Clustered column chart |
| PHMSA incident count by year | `tblPHMSAIncidentRisk` | Line or column chart |
| PHMSA incident count by cause category if available | `tblPHMSAIncidentRisk` | Horizontal bar chart |
| Compressor oil temperature trend if datetime column exists | `tblMetroPT3CompressorSample` | Line chart |
| Compressor pressure trend if available | `tblMetroPT3CompressorSample` | Line chart with `TP2`, `TP3`, or `Reservoirs` |

## Suggested Slicers

Use slicers on Pivot Tables where possible:

- `lng_equipment_category`
- `maintenance_priority`
- `source_dataset`
- `year`

Optional slicers:

- `cause_category_if_available`
- `state_or_location_field_if_available`
- `release_or_leak_field_if_available`

## Pivot Table Guidance

### Azure Asset Health By Category

- Source: `tblAzureReliabilitySummary`
- Rows: `lng_equipment_category`
- Values: Average of `asset_health_score`
- Optional slicer: `maintenance_priority`

### Maintenance Priority Count

- Source: `tblAzureReliabilitySummary`
- Rows: `maintenance_priority`
- Values: Count of `lng_asset_id`
- Sort order: Critical, High, Medium, Low

### Failure Count By Asset

- Source: `tblAzureReliabilitySummary`
- Rows: `lng_asset_id` or `lng_asset_name`
- Values: Sum of `failure_count`
- Filter or sort: Top 10 by failure count

### PHMSA Incident Count By Year

- Source: `tblPHMSAIncidentRisk`
- Rows: `year`
- Columns or slicer: `source_dataset`
- Values: Sum of `incident_count`

### PHMSA Incident Count By Cause

- Source: `tblPHMSAIncidentRisk`
- Rows: `cause_category_if_available`
- Values: Sum of `incident_count`
- Filter: remove or group `Not available` if needed

### Compressor Trends

For the MetroPT-3 sample, a normal Excel line chart may be simpler than a Pivot
Chart:

- X axis: `timestamp`
- Series: `Oil_temperature`
- Optional pressure series: `TP2`, `TP3`, `Reservoirs`
- Optional load series: `Motor_current`

## Suggested Helper Calculations

Place helper calculations on `KPI_Calculations`.

| Calculation | Example Formula |
|---|---|
| Critical asset percentage | `=COUNTIF(tblAzureReliabilitySummary[maintenance_priority],"Critical")/ROWS(tblAzureReliabilitySummary[machineID])` |
| High or critical asset count | `=COUNTIF(tblAzureReliabilitySummary[maintenance_priority],"Critical")+COUNTIF(tblAzureReliabilitySummary[maintenance_priority],"High")` |
| Average failures per asset | `=AVERAGE(tblAzureReliabilitySummary[failure_count])` |
| Total PHMSA estimated cost | `=SUM(tblPHMSAIncidentRisk[total_estimated_cost_if_available])` |
| Total PHMSA injuries | `=SUM(tblPHMSAIncidentRisk[injuries_if_available])` |
| Average compressor oil temperature | `=AVERAGE(tblMetroPT3CompressorSample[Oil_temperature])` |
| Average compressor motor current | `=AVERAGE(tblMetroPT3CompressorSample[Motor_current])` |

## AI Recommendations Sheet

The `AI_Recommendations` sheet should be optional and clearly labeled. Suggested
columns:

- `recommendation_id`
- `source_section`
- `finding`
- `suggested_action`
- `engineering_caveat`
- `review_status`

Required wording:

`Generated for portfolio demonstration using public industrial datasets. Review
by a qualified engineer would be required before any real operational use.`

## Assumptions Sheet

The `Assumptions` sheet should include:

- Public datasets are adapted into LNG-style reliability categories.
- This is not ExxonMobil or PNG LNG operating data.
- Azure MTBF-style, MTTR-style, and availability-style values are estimates.
- PHMSA outputs are risk-awareness summaries, not formal integrity assessments.
- MetroPT-3 compressor trends are process-surveillance examples, not LNG plant
  alarm limits.
- The workbook is not connected to live plant systems or a CMMS.

## Workbook Notes

This workbook is an operations technical portfolio dashboard. It is designed to
show data handling, reliability thinking, chart design, and engineering
communication. It should not be presented as a live plant dashboard, regulatory
assessment, or operator reliability report.
