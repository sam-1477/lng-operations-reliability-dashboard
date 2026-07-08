# Data Dictionary

This directory contains all data for the LNG Operations Technical Reliability Dashboard.

## Directory Structure

```
data/
├── raw/           # Unmodified downloaded datasets (NOT committed to Git)
│   ├── phmsa_incidents.csv
│   ├── metropt3/         # MetroPT-3 extracted sensor files
│   └── azure_pdm/        # Azure PdM extracted CSVs
├── processed/     # Cleaned and transformed data (committed to Git)
│   ├── asset_register.csv
│   ├── downtime_log.csv
│   ├── failure_summary.csv
│   ├── compressor_health.csv
│   ├── pipeline_risk_scores.csv
│   └── reliability_kpis.csv
└── README.md      # This file
```

## Processed Data Files

### asset_register.csv
The mapped LNG asset register. Each row is one asset.

| Column | Type | Description |
|--------|------|-------------|
| asset_id | str | Unique identifier (e.g., LNG-COMP-001) |
| asset_name | str | Human-readable name |
| lng_category | str | LNG equipment category (see below) |
| subsystem | str | Plant subsystem |
| criticality | str | A (critical), B (major), C (minor) |
| install_date | date | In-service date |
| source_dataset | str | Which public dataset this asset came from |

LNG Categories: Compressor Train, Gas Turbine, Centrifugal Pump, Air-Cooled HX,
Cryogenic HX, Pressure Vessel, Storage Tank, Pipeline, Instrumentation & Control,
Electrical System

### downtime_log.csv
All recorded downtime events.

| Column | Type | Description |
|--------|------|-------------|
| event_id | str | Unique event identifier |
| asset_id | str | FK to asset_register |
| start_time | datetime | Downtime start |
| end_time | datetime | Downtime end |
| duration_hours | float | End - Start in hours |
| failure_mode | str | Bearing, Seal Leak, Overheating, Vibration, Electrical, etc. |
| consequence | str | None, Minor, Significant, Major |
| source_dataset | str | Data provenance |

### failure_summary.csv
Aggregated failure statistics by asset and failure mode.

| Column | Type | Description |
|--------|------|-------------|
| asset_id | str | FK to asset_register |
| failure_mode | str | Failure category |
| failure_count | int | Number of occurrences |
| total_downtime_hours | float | Sum of all downtime for this failure mode |
| date_range_start | date | First failure in window |
| date_range_end | date | Last failure in window |

### compressor_health.csv
MetroPT-3 data resampled to 1-minute with derived health indicators.

| Column | Type | Description |
|--------|------|-------------|
| timestamp | datetime | Resampled timestamp (1-min intervals) |
| pressure_bar | float | Suction pressure |
| temperature_c | float | Discharge temperature |
| vibration_mms | float | Vibration RMS |
| motor_current_a | float | Motor current |
| rpm | float | Shaft speed |
| vib_rolling_mean | float | 1-hour rolling mean of vibration |
| vib_rolling_std | float | 1-hour rolling std of vibration |
| anomaly_flag | bool | Exceeds 2 from rolling mean |

### pipeline_risk_scores.csv
PHMSA incident data filtered, cleaned, and scored.

| Column | Type | Description |
|--------|------|-------------|
| incident_id | str | PHMSA incident number |
| incident_date | date | Date of incident |
| root_cause | str | Mapped LNG cause category |
| consequence_score | int | 0–3 numeric consequence |
| likelihood_score | float | Estimated frequency score |
| risk_index | float | likelihood + consequence |

### reliability_kpis.csv
Computed reliability KPIs at asset and category level.

| Column | Type | Description |
|--------|------|-------------|
| scope | str | Plant, Category, or Asset |
| scope_name | str | Category name or asset_id |
| failure_count | int | Number of failures |
| total_downtime_hours | float | Sum of downtime |
| mttr_hours | float | Mean Time To Repair |
| mtbf_days | float | Mean Time Between Failures (estimated) |
| availability_pct | float | Availability as percentage |
| failure_rate_1khrs | float | Failure rate per 1000 operating hours |

---

## Data Provenance

All data derived from publicly available sources. See `docs/data_sources.md` for
full attribution, download links, and license information.

**No confidential, proprietary, or licensee data is present in this repository.**