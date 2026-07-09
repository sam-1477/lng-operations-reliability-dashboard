# Azure Reliability Summary Report

## What The Script Does

`scripts/build_azure_reliability_summary.py` reads the public Azure Predictive Maintenance dataset and builds one dashboard-ready reliability summary row per machine. The output is written to `data/processed/azure_machine_reliability_summary.csv`, and a GitHub-safe sample is written to `samples/azure/azure_machine_reliability_summary_sample.csv`.

The Azure machines are mapped into LNG-style equipment categories for portfolio demonstration. This is an adapted public dataset; it does not use ExxonMobil, PNG LNG, confidential, proprietary, or licensee data.

## Source Files Used

- `data/raw/extracted/azure_pdm/PdM_machines.csv`
- `data/raw/extracted/azure_pdm/PdM_telemetry.csv`
- `data/raw/extracted/azure_pdm/PdM_errors.csv`
- `data/raw/extracted/azure_pdm/PdM_failures.csv`
- `data/raw/extracted/azure_pdm/PdM_maint.csv`

The script reads these files only. It does not modify raw data.

## Reliability KPIs Calculated

- Telemetry record count as an operating-hour proxy
- Average voltage, rotation, pressure, and vibration
- Error count
- Maintenance event count
- Failure count
- Last recorded failure type
- Estimated downtime hours
- MTBF-style hours
- MTTR-style hours
- Availability-style percent
- Asset health score
- Maintenance priority
- Engineering note

## Assumptions Used

- Each failure is assumed to cause 8 downtime hours.
- Telemetry record count is used as a simple operating-hour proxy.
- MTBF-style estimate equals telemetry record count divided by failure count when failures exist.
- MTTR-style estimate equals estimated downtime divided by failure count when failures exist.
- Availability-style estimate uses telemetry records as the operating basis and estimated downtime as unavailable time.
- Asset health score starts at 100 and subtracts points for failures, errors, maintenance events, and above-average vibration.
- LNG-style asset IDs and equipment categories are demonstration mappings applied to public Azure machines.

## Dashboard Usefulness

This table gives the LNG Operations Technical Reliability Dashboard a first machine-level reliability layer. It can support dashboard views for asset ranking, maintenance priority filtering, health score comparison, and quick review of repeated failures or high sensor averages.

## Limitations

- These are MTBF-style, MTTR-style, and availability-style estimates, not formal plant reliability calculations.
- The Azure dataset is public predictive maintenance data, not LNG plant operating history.
- The LNG equipment categories are adapted labels for portfolio use.
- Downtime is estimated with a fixed 8-hour assumption per failure.
- Telemetry row count is only a proxy for operating hours.
- The health score is a simple screening score, not a validated risk model.

## Output Snapshot

- Machine rows created: 100
- Average asset health score: 10.3
- Minimum asset health score: 0.0
- Maximum asset health score: 79.1
- Maintenance priority counts:
- Critical: 98
- Medium: 2
