# Data Sources

All data used in this project is **publicly available**. No proprietary, confidential,
or licensee data is used. Each dataset is attributed to its original source.

---

## Dataset 1: PHMSA Gas Transmission & LNG Incident Data

| Field | Detail |
|-------|--------|
| **Full Name** | PHMSA Gas Transmission and Gathering Incident Data |
| **Publisher** | U.S. Department of Transportation — Pipeline and Hazardous Materials Safety Administration (PHMSA) |
| **Source URL** | https://www.phmsa.dot.gov/data-and-statistics/pipeline/gas-transmission-and-gathering-incident-data |
| **Format** | CSV / Excel |
| **Coverage** | 1970–present (we use 2010–2024 for relevance) |
| **License** | U.S. Government public data (no restrictions) |
| **Size** | ~10,000 rows |
| **Key Fields Used** | Incident date, location, cause category, consequence, pipeline type, commodity |
| **Why This Dataset** | Real regulatory incident data with root cause classification — demonstrates process safety and pipeline risk thinking directly applicable to LNG feed/product pipelines |

### LNG Adaptation Notes

- Filtered to: Gas Transmission (onshore) + LNG Facility incidents
- Root cause categories mapped to LNG-recognized failure modes
- Consequence data used for risk matrix scoring
- Geographic data NOT used (U.S. locations not relevant to PNG context)

---

## Dataset 2: MetroPT-3 Compressor Predictive Maintenance

| Field | Detail |
|-------|--------|
| **Full Name** | MetroPT-3: A Benchmark Dataset for Predictive Maintenance |
| **Publisher** | Metropolitan Public Transport of Porto / FEUP, University of Porto |
| **Source URL** | https://archive.ics.uci.edu/dataset/791/metropt-3+dataset |
| **Format** | CSV (multiple files) |
| **Coverage** | Multi-month continuous sensor data at 1 Hz |
| **License** | Creative Commons Attribution 4.0 International (CC BY 4.0) |
| **Size** | ~1.5 GB (raw), ~50 MB (processed/resampled) |
| **Key Fields Used** | Pressure (bar), temperature (°C), vibration (mm/s RMS), motor current (A), RPM |
| **Why This Dataset** | Real industrial sensor data from a compressor — the closest public proxy to LNG refrigerant compressor condition monitoring |

### Research Paper

Veloso, B., Gama, J., Ribeiro, R.P., Pereira, P.M. (2022). "The MetroPT dataset for predictive maintenance." *Scientific Data*, 9, 764.

### LNG Adaptation Notes

- Air compressor sensor data adapted to "LNG Propane Compressor A"
- Sensor names and units preserved (they are the same measurements)
- Known fault periods used as ground truth labels
- Dataset documentation: https://github.com/bveloso/metropt-3-dataset

---

## Dataset 3: Microsoft Azure Predictive Maintenance

| Field | Detail |
|-------|--------|
| **Full Name** | Predictive Maintenance Modeling Dataset |
| **Publisher** | Microsoft Azure AI / Kaggle |
| **Source URL** | https://www.kaggle.com/datasets/arnabbiswas1/microsoft-azure-predictive-maintenance |
| **Format** | CSV (5 tables: telemetry, errors, maintenance, machines, failures) |
| **Coverage** | 100 machines over 1 year |
| **License** | Database Contents License (DbCL) v1.0 |
| **Size** | ~700 MB |
| **Key Fields Used** | Machine ID, error codes, failure timestamps, maintenance actions, machine age, machine model |
| **Why This Dataset** | Provides the maintenance-log and failure-history dimension that MetroPT-3 lacks — enables MTTR/MTBF computation and maintenance priority ranking |

### LNG Adaptation Notes

- Machine models mapped to LNG equipment categories (see `src/lng_mappings.py`)
- Error codes interpreted as failure modes (bearing, seal, overheating, vibration)
- Maintenance records used as "work order" analog
- Failure timestamps used for downtime calculation

---

## Data Attribution Summary

| Dataset | Attribution Required? | Attribution Statement |
|---------|----------------------|----------------------|
| PHMSA Incident Data | No (U.S. Govt) | "Source: U.S. DOT PHMSA" on all derivative work |
| MetroPT-3 | Yes (CC BY 4.0) | "Based on MetroPT-3 dataset by Veloso et al. (2022), CC BY 4.0" |
| Azure PdM | Yes (DbCL) | "Based on Microsoft Azure Predictive Maintenance dataset" |

---

## Download Instructions

### PHMSA Data
1. Visit https://www.phmsa.dot.gov/data-and-statistics/pipeline/gas-transmission-and-gathering-incident-data
2. Download "Gas Transmission and Gathering Incident Data — All Years" (Excel or CSV)
3. Save as `data/raw/phmsa_incidents.csv`

### MetroPT-3
1. Visit https://archive.ics.uci.edu/dataset/791/metropt-3+dataset
2. Download the ZIP file
3. Extract all sensor CSV files into `data/raw/metropt3/`

### Azure PdM
1. Visit https://www.kaggle.com/datasets/arnabbiswas1/microsoft-azure-predictive-maintenance
2. Download the ZIP
3. Extract all 5 CSV files into `data/raw/azure_pdm/`

---

*Last updated: July 2026*