# Excel Dashboard Build Report

## Workbook Created

- Workbook: `excel/lng_operations_reliability_dashboard.xlsx`
- Status: polished starter/skeleton workbook, not a live plant dashboard
- Purpose: operations technical reliability dashboard portfolio demonstration
- Visual polish: visible worksheet-level chart headings, dashboard title band, KPI cards, gridline visibility, KPI tables, and AI recommendation formatting were improved.
- Theme: professional red/navy/white/light-gray energy-sector dashboard theme.
- Branding boundary: no ExxonMobil logos, trademarks, or official brand assets were used.

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

- Maintenance priority count, with Critical red and Medium muted gray as separate chart series
- Asset health by LNG equipment category, shown as a horizontal multi-color bar chart with readable category labels and no obstructive category-axis title
- PHMSA incident count by year, corrected as a single-series red column chart with Year as the x-axis category, visible x-axis year labels, and visible horizontal chart gridlines for readability

Dashboard visual polish was applied with a large navy title band, a subtitle, a visible red disclaimer area, merged KPI cards, worksheet-level chart headings, clearer chart spacing, hidden worksheet gridlines, and red/navy accent colors. The Maintenance Priority Count chart uses separate series so Critical is red and Medium is muted gray, with readable priority labels and a compact legend. The Asset Health By LNG Equipment Category chart was changed to a horizontal bar chart so category labels remain readable, each category uses a distinct muted navy, red, steel, gray, or teal fill, and the obstructive Equipment Category axis title was removed. The PHMSA Incident Count By Year chart was corrected so Year is used as the x-axis category, Incident Count is one meaningful data series, and every annual x-axis label is requested for Microsoft 365 Excel display. The previous year-by-year legend issue was fixed by using a Dashboard-local two-column chart source and removing the legend. The PHMSA chart height and x-axis layout were adjusted so the year labels have more room below the red columns. Horizontal chart gridlines were enabled to make the year-to-year incident trend easier to read. Native chart title and axis text styling is also attempted through openpyxl, but the worksheet headings provide a reliable visible fallback in Excel.

## Formatting Improvements

- `KPI_Calculations` uses plain-text formula guidance instead of broken `#REF!` references.
- `KPI_Calculations` keeps current calculated values while applying a large title, red accent line, navy header row, white bold header text, light-gray calculation rows, borders, fixed widths, wrapped notes, and freeze panes.
- `AI_Recommendations` uses a large title, red accent line, navy header row, white bold header text, text wrapping, row heights sized for wrapped text, requested column widths, and freeze panes below the header.
- The workbook opens on the `Dashboard` sheet and hides worksheet gridlines to reduce visual clutter.
- Maintenance Priority bars were given distinct colors through separate chart series: Critical uses energy red and Medium uses muted gray.
- Maintenance Priority chart axis count visibility was improved with a 0-based y-axis, visible 20-unit major ticks, numeric labels, and horizontal gridlines.
- Maintenance Priority Count y-axis label readability was fixed by removing the native chart title and placing a separate worksheet `Asset Count` label outside the chart; the y-axis numeric scale remains visible.
- Asset Health equipment categories were given distinct colors through separate chart series using a consistent navy, red, steel blue, gray, and muted teal palette.
- Asset Health chart legend/category readability was improved with a visible right-side legend and readable left-side category labels.
- Obstructive x-axis label placement was fixed by removing the Asset Health `Equipment Category` axis title and leaving the category labels on the left category axis.
- PHMSA chart layout was enlarged and adjusted so its Year and Incident Count axis labels remain readable.
- Dashboard chart spacing was improved to prevent overlap with section headers and preserve clean screenshot framing.
- Worksheet gridlines remain hidden; the PHMSA chart gridlines are chart-internal horizontal major gridlines only.
- The PHMSA chart uses a clean column chart because Microsoft 365 was not reliably rendering the previous line-chart gridlines or legend orientation.
- PHMSA chart x-axis year labels were made visible with bottom tick-label placement and no major tick-label skipping.
- PHMSA chart height/layout was adjusted for readability; the x-axis title remains `Year` and the y-axis title remains `Incident Count`.
- The former `Manual Excel Work Remaining` table was removed from the Dashboard and moved to the `Assumptions` sheet under `Future Manual Enhancements`, covering slicers, formatting polish, chart refinement, and validation.
- Dashboard freeze panes were removed so the header no longer obstructs scrolling or screenshot capture.
- Data sheets keep frozen headers and readable table formatting with consistent navy header styling where practical.

## Assumptions

- Azure machines are mapped into LNG-style asset categories.
- Telemetry record count is used as an operating-hour proxy.
- Each failure is assumed to cause 8 downtime hours.
- MTBF-style and availability-style values are estimates for portfolio learning.
- MetroPT-3 is adapted for LNG-style compressor surveillance.
- PHMSA is public US incident data used for risk-awareness context.
- The workbook is not a formal mechanical integrity assessment or live plant dashboard.

## Future Manual Enhancements

The former `Manual Excel Work Remaining` content was moved from the Dashboard to the `Assumptions` sheet under `Future Manual Enhancements`.
- Slicers for maintenance priority, LNG equipment category, source dataset, and year.
- Formatting polish for print area, spacing, number formats, and screenshot framing.
- Chart refinement review for labels, titles, axis scales, and native Excel rendering.
- Validation of assumptions and portfolio wording before publication.

## Portfolio Story Support

This workbook connects Azure reliability scoring, MetroPT-3 compressor surveillance, and PHMSA incident risk awareness into one operations technical reliability dashboard. It demonstrates data preparation, reliability thinking, risk-awareness communication, and Excel-based presentation using public industrial datasets adapted into LNG-style reliability categories. The workbook remains a portfolio demonstration using public datasets, not ExxonMobil or PNG LNG operating data.
