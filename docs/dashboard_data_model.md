# Dashboard Data Model

This document connects the processed public industrial datasets into the data
model for the LNG Operations Technical Reliability Dashboard. The project uses
public datasets adapted into LNG-style reliability categories for portfolio
demonstration.

The dashboard is not ExxonMobil or PNG LNG operating data. It is an operations
technical reliability dashboard built to demonstrate reliability analysis,
incident risk awareness, and compressor surveillance methods.

## Datasets Used

| Dataset | Public Source | Dashboard Role | Current Local Dashboard Input |
|---|---|---|---|
| Azure Predictive Maintenance | Microsoft / Kaggle public dataset | Machine reliability, maintenance priority, asset health scoring | `data/processed/azure_machine_reliability_summary.csv` |
| PHMSA LNG Incidents | U.S. DOT PHMSA public incident data | LNG incident awareness and consequence context | `data/processed/phmsa_incident_risk_summary.csv` |
| PHMSA Gas Transmission Incidents | U.S. DOT PHMSA public incident data | Pipeline incident trends and mechanical integrity context | `data/processed/phmsa_incident_risk_summary.csv` |
| MetroPT-3 Compressor | UCI / public compressor dataset | Compressor process surveillance and rotating equipment monitoring | `samples/metropt3/metropt3_compressor_sample.csv` |

## Dashboard Input Files

| File | Rows Currently Available | Intended Excel Sheet | Suggested Excel Table Name |
|---|---:|---|---|
| `data/processed/azure_machine_reliability_summary.csv` | 100 | `Azure_Reliability_Summary` | `tblAzureReliabilitySummary` |
| `data/processed/phmsa_incident_risk_summary.csv` | 1,564 | `PHMSA_Incident_Risk` | `tblPHMSAIncidentRisk` |
| `samples/metropt3/metropt3_compressor_sample.csv` | 1,000 | `MetroPT3_Compressor_Sample` | `tblMetroPT3CompressorSample` |
| `samples/azure/azure_machine_reliability_summary_sample.csv` | 100 | Optional reviewer sample | `tblAzureReliabilitySample` |
| `samples/phmsa/phmsa_lng_incident_sample.csv` | 51 | Optional reviewer sample | `tblPHMSALNGSample` |
| `samples/phmsa/phmsa_gas_transmission_incident_sample.csv` | 500 | Optional reviewer sample | `tblPHMSAGasTransmissionSample` |

## Dashboard Sections Supported

### Azure Reliability Summary

Azure provides the asset-level reliability and maintenance-priority section. It
maps public machine IDs into LNG-style equipment categories such as Process
Pumps, Gas Compressors, Electric Motors, Utility Generators, and Cooling Water
Pumps.

Useful dashboard views:

- Total assets
- Critical and high-priority asset counts
- Average asset health score
- Estimated downtime hours
- Asset health by LNG equipment category
- Failure count by asset
- Maintenance priority count
- Average vibration by equipment category

### PHMSA Incident Risk

PHMSA provides public incident risk context for LNG facility and pipeline
awareness. It supports a risk-awareness summary, not a formal integrity
assessment.

Useful dashboard views:

- Incident count by source dataset
- Incident count by year
- Incident count by cause category if available
- Estimated cost by year or cause
- Fatalities and injuries by grouped incident category
- Ignition/fire and release/leak screening views

### MetroPT-3 Compressor Sample

MetroPT-3 provides a public compressor dataset adapted for LNG-style compressor
surveillance. It gives the dashboard a process-monitoring section for trends and
screening flags.

Useful dashboard views:

- Compressor sample records
- Oil temperature trend
- Motor current trend
- Pressure trends using `TP2`, `TP3`, `H1`, `DV_pressure`, and `Reservoirs`
- Operating status signals using `COMP`, `DV_eletric`, `Pressure_switch`,
  `Oil_level`, and related binary fields

## Key Fields

### `tblAzureReliabilitySummary`

| Field | Purpose |
|---|---|
| `machineID` | Source machine identifier from Azure PdM |
| `lng_asset_id` | LNG-style asset identifier for dashboard display |
| `lng_asset_name` | Human-readable mapped asset name |
| `lng_equipment_category` | Main slicer and grouping field |
| `maintenance_priority` | Main asset-priority slicer |
| `asset_health_score` | KPI and chart value |
| `failure_count` | Reliability event count |
| `estimated_downtime_hours` | Downtime-style KPI |
| `avg_vibration` | Rotating equipment condition indicator |
| `engineering_note` | Short dashboard text note |

### `tblPHMSAIncidentRisk`

| Field | Purpose |
|---|---|
| `source_dataset` | Separates LNG and Gas Transmission PHMSA sources |
| `year` | Time trend and slicer field |
| `state_or_location_field_if_available` | Geographic or location grouping where available |
| `cause_category_if_available` | Cause-category charting and review |
| `incident_type_or_system_type_if_available` | System or asset-context grouping |
| `incident_count` | Incident count KPI and chart value |
| `total_estimated_cost_if_available` | Consequence cost indicator |
| `fatalities_if_available` | Consequence severity indicator |
| `injuries_if_available` | Consequence severity indicator |
| `ignition_or_fire_field_if_available` | Fire/ignition screening field |
| `release_or_leak_field_if_available` | Release/leak screening field |
| `dashboard_risk_note` | Short risk-awareness note |

### `tblMetroPT3CompressorSample`

| Field | Purpose |
|---|---|
| `timestamp` | Time-series trend axis |
| `TP2` | Pressure trend candidate |
| `TP3` | Pressure trend candidate |
| `H1` | Pressure or system-state trend candidate |
| `DV_pressure` | Discharge valve pressure trend candidate |
| `Reservoirs` | Reservoir pressure trend candidate |
| `Oil_temperature` | Oil temperature trend and alert candidate |
| `Motor_current` | Compressor load and operating-state indicator |
| `COMP` | Compressor status signal |
| `Pressure_switch` | Pressure switch status signal |
| `Oil_level` | Oil level status signal |

## Suggested Relationships And Lookups

This dashboard should use a simple Excel model. The datasets come from different
public sources, so the workbook should avoid forcing artificial joins where no
real common key exists.

| Relationship Type | Suggested Approach |
|---|---|
| Azure asset KPIs to dashboard cards | Direct formulas and Pivot Tables from `tblAzureReliabilitySummary` |
| Azure category slicer | Use `lng_equipment_category` to filter Azure charts and KPI cards |
| Azure priority slicer | Use `maintenance_priority` to filter asset health and failure views |
| PHMSA source slicer | Use `source_dataset` to separate LNG incidents from Gas Transmission incidents |
| PHMSA year slicer | Use `year` for incident trend charts |
| PHMSA cause slicer | Use `cause_category_if_available` where available |
| MetroPT-3 trend axis | Use `timestamp` directly for compressor trends |
| Cross-source comparison | Use dashboard sections side by side, not a relational join |

Optional helper tables:

- `tblEquipmentCategoryLookup`: maps `lng_equipment_category` to dashboard color,
  display order, and broad asset family.
- `tblPriorityLookup`: maps `maintenance_priority` to sort order and red/amber/green
  colors.
- `tblSourceDatasetLookup`: maps PHMSA source labels to shorter chart labels.
- `tblAssumptions`: lists public-data assumptions and wording to show in the workbook.

## Recommended Data Model Boundaries

The Azure table is the only table with asset-level rows. The PHMSA and MetroPT-3
tables should be treated as supporting evidence for incident awareness and
process surveillance methods.

Do not join PHMSA incident rows directly to Azure assets. PHMSA incidents are
real public US incident records, while Azure assets are public predictive
maintenance machines mapped into LNG-style categories.

Do not join MetroPT-3 compressor rows directly to Azure assets. MetroPT-3 is a
public compressor dataset used to demonstrate process-surveillance trending.

## Limitations Of Combining Public Datasets

- The datasets come from different industries, equipment, countries, and
  reporting structures.
- Azure machine IDs are not real LNG asset IDs.
- MetroPT-3 is an air compressor dataset, not an LNG refrigerant or boil-off gas
  compressor dataset.
- PHMSA data is US regulatory incident data, not PNG LNG operating data.
- MTBF-style, MTTR-style, availability-style, and risk-awareness outputs are
  screening metrics for portfolio demonstration.
- Cross-source dashboard views should be presented as an integrated portfolio
  demonstration, not as a single real plant data model.
