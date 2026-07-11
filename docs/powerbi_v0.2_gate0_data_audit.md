# Power BI v0.2 Gate 0 Data Audit

Audit date: 2026-07-11

Scope:
- Folder inspected: `data\processed`
- CSV files inspected: 2
- Non-CSV files ignored: `.gitkeep`
- No CSV files were changed.
- No synthetic data was generated.
- No PBIX file was built or edited.

## Executive Verdict

**Readiness verdict:** Not ready - missing required tables.

The current `data\processed` folder contains two summary-level CSV files:

1. `azure_machine_reliability_summary.csv`
2. `phmsa_incident_risk_summary.csv`

These files are useful portfolio source summaries, but they do not provide the
transaction-level fact tables required for the Power BI v0.2 star schema. The
available Azure summary can support a draft `dim_Asset` after renaming and
adding missing asset attributes. It cannot replace event-level failure,
maintenance, or PM compliance fact tables.

## 1. File Inventory

### 1.1 `azure_machine_reliability_summary.csv`

**Row count:** 100

**Column count:** 22

**Exact column names:**

```text
machineID
model
age
lng_asset_id
lng_asset_name
lng_equipment_category
telemetry_record_count
avg_voltage
avg_rotate
avg_pressure
avg_vibration
error_count
maintenance_event_count
failure_count
last_failure_type
estimated_downtime_hours
mtbf_style_hours
mttr_style_hours
availability_style_percent
asset_health_score
maintenance_priority
engineering_note
```

**Detected data types:**

| Column | Detected type |
|---|---|
| machineID | Whole Number |
| model | Text |
| age | Whole Number |
| lng_asset_id | Text |
| lng_asset_name | Text |
| lng_equipment_category | Text |
| telemetry_record_count | Whole Number |
| avg_voltage | Decimal Number |
| avg_rotate | Decimal Number |
| avg_pressure | Decimal Number |
| avg_vibration | Decimal Number |
| error_count | Whole Number |
| maintenance_event_count | Whole Number |
| failure_count | Whole Number |
| last_failure_type | Text |
| estimated_downtime_hours | Whole Number |
| mtbf_style_hours | Decimal Number |
| mttr_style_hours | Decimal Number |
| availability_style_percent | Decimal Number |
| asset_health_score | Decimal Number |
| maintenance_priority | Text |
| engineering_note | Text |

**First 3 sample rows:**

```json
[
  {
    "machineID": "1",
    "model": "model3",
    "age": "18",
    "lng_asset_id": "LNG-PMP-001",
    "lng_asset_name": "Process Pump 001",
    "lng_equipment_category": "Process Pumps",
    "telemetry_record_count": "8761",
    "avg_voltage": "170.83",
    "avg_rotate": "446.34",
    "avg_pressure": "100.67",
    "avg_vibration": "40.59",
    "error_count": "35",
    "maintenance_event_count": "37",
    "failure_count": "7",
    "last_failure_type": "comp4",
    "estimated_downtime_hours": "56",
    "mtbf_style_hours": "1251.57",
    "mttr_style_hours": "8.0",
    "availability_style_percent": "99.36",
    "asset_health_score": "0.0",
    "maintenance_priority": "Critical",
    "engineering_note": "Review immediately. Repeated failures or poor health score detected."
  },
  {
    "machineID": "2",
    "model": "model4",
    "age": "7",
    "lng_asset_id": "LNG-CMP-002",
    "lng_asset_name": "Gas Compressor 002",
    "lng_equipment_category": "Gas Compressors",
    "telemetry_record_count": "8761",
    "avg_voltage": "170.76",
    "avg_rotate": "446.39",
    "avg_pressure": "100.54",
    "avg_vibration": "40.3",
    "error_count": "28",
    "maintenance_event_count": "32",
    "failure_count": "4",
    "last_failure_type": "comp2",
    "estimated_downtime_hours": "32",
    "mtbf_style_hours": "2190.25",
    "mttr_style_hours": "8.0",
    "availability_style_percent": "99.63",
    "asset_health_score": "30.4",
    "maintenance_priority": "Critical",
    "engineering_note": "Review immediately. Repeated failures or poor health score detected."
  },
  {
    "machineID": "3",
    "model": "model3",
    "age": "8",
    "lng_asset_id": "LNG-MTR-003",
    "lng_asset_name": "Electric Motor 003",
    "lng_equipment_category": "Electric Motors",
    "telemetry_record_count": "8761",
    "avg_voltage": "170.66",
    "avg_rotate": "446.58",
    "avg_pressure": "100.65",
    "avg_vibration": "40.48",
    "error_count": "39",
    "maintenance_event_count": "37",
    "failure_count": "5",
    "last_failure_type": "comp2",
    "estimated_downtime_hours": "40",
    "mtbf_style_hours": "1752.2",
    "mttr_style_hours": "8.0",
    "availability_style_percent": "99.54",
    "asset_health_score": "13.7",
    "maintenance_priority": "Critical",
    "engineering_note": "Review immediately. Repeated failures or poor health score detected."
  }
]
```

### 1.2 `phmsa_incident_risk_summary.csv`

**Row count:** 1,564

**Column count:** 12

**Exact column names:**

```text
source_dataset
incident_count
year
state_or_location_field_if_available
cause_category_if_available
incident_type_or_system_type_if_available
total_estimated_cost_if_available
fatalities_if_available
injuries_if_available
ignition_or_fire_field_if_available
release_or_leak_field_if_available
dashboard_risk_note
```

**Detected data types:**

| Column | Detected type |
|---|---|
| source_dataset | Text |
| incident_count | Whole Number |
| year | Whole Number |
| state_or_location_field_if_available | Text |
| cause_category_if_available | Text |
| incident_type_or_system_type_if_available | Text |
| total_estimated_cost_if_available | Whole Number |
| fatalities_if_available | Whole Number |
| injuries_if_available | Whole Number |
| ignition_or_fire_field_if_available | Boolean-like text |
| release_or_leak_field_if_available | Text |
| dashboard_risk_note | Text |

**First 3 sample rows:**

```json
[
  {
    "source_dataset": "PHMSA Gas Transmission Incidents",
    "incident_count": "15",
    "year": "2010",
    "state_or_location_field_if_available": "Not available",
    "cause_category_if_available": "CORROSION FAILURE",
    "incident_type_or_system_type_if_available": "TRANSMISSION SYSTEM",
    "total_estimated_cost_if_available": "6648492",
    "fatalities_if_available": "0",
    "injuries_if_available": "0",
    "ignition_or_fire_field_if_available": "NO",
    "release_or_leak_field_if_available": "LEAK",
    "dashboard_risk_note": "High reported cost group. Review consequence severity and controls."
  },
  {
    "source_dataset": "PHMSA Gas Transmission Incidents",
    "incident_count": "4",
    "year": "2010",
    "state_or_location_field_if_available": "OK",
    "cause_category_if_available": "EQUIPMENT FAILURE",
    "incident_type_or_system_type_if_available": "TRANSMISSION SYSTEM",
    "total_estimated_cost_if_available": "305357",
    "fatalities_if_available": "0",
    "injuries_if_available": "0",
    "ignition_or_fire_field_if_available": "NO",
    "release_or_leak_field_if_available": "OTHER",
    "dashboard_risk_note": "Mechanical integrity theme. Review cause category and asset context."
  },
  {
    "source_dataset": "PHMSA Gas Transmission Incidents",
    "incident_count": "3",
    "year": "2010",
    "state_or_location_field_if_available": "LA",
    "cause_category_if_available": "MATERIAL FAILURE OF PIPE OR WELD",
    "incident_type_or_system_type_if_available": "TRANSMISSION SYSTEM",
    "total_estimated_cost_if_available": "1053748",
    "fatalities_if_available": "0",
    "injuries_if_available": "0",
    "ignition_or_fire_field_if_available": "NO",
    "release_or_leak_field_if_available": "LEAK",
    "dashboard_risk_note": "High reported cost group. Review consequence severity and controls."
  }
]
```

## 2. Required Power BI Table Mapping

### 2.1 Mapping summary

| Proposed Power BI table | Source filename | Exists in processed data? | Result |
|---|---|---:|---|
| dim_Asset | `azure_machine_reliability_summary.csv` | Partial | Usable only after renaming and adding missing asset attributes |
| fact_Failure | None | No | Missing required event-level failure table |
| fact_Maintenance | None | No | Missing required work-order maintenance table |
| fact_PM_Compliance | None | No | Missing required PM compliance table |
| dim_FailureMode | None | No | Optional lookup missing; can be created only if source failure modes are available |
| dim_MaintenanceAction | None | No | Optional lookup missing; no source action lookup exists |

### 2.2 `dim_Asset`

**Source filename:** `azure_machine_reliability_summary.csv`

**Exists:** Partial source exists.

**Required columns present directly:** None using final Power BI names.

**Columns that need renaming:**

| Required column | Source column |
|---|---|
| AssetID | lng_asset_id |
| AssetName | lng_asset_name |
| EquipmentCategory | lng_equipment_category |

**Columns that need creating:**

| Required column | Status |
|---|---|
| CategoryGroup | Must be created from an approved category grouping rule |
| CriticalityRating | Must be created or mapped from an approved criticality rule; `maintenance_priority` is not a direct replacement |
| Subsystem | Must be created or sourced |
| Location | Must be created or sourced |

**Columns missing:** `CategoryGroup`, `CriticalityRating`, `Subsystem`, `Location`

### 2.3 `fact_Failure`

**Source filename:** None.

**Exists:** No.

`azure_machine_reliability_summary.csv` contains asset-level summary fields such
as `failure_count`, `last_failure_type`, `estimated_downtime_hours`,
`mtbf_style_hours`, and `mttr_style_hours`. These are not event-level records and
cannot safely become `fact_Failure`.

**Columns that need renaming:** None. No valid event-level source exists.

**Columns that need creating:** A complete event-level failure fact table must be
created from source data, not from aggregate summaries.

**Columns missing:**

```text
EventID
AssetID
FailureDate
FailureModeID or FailureMode
DowntimeStart
DowntimeEnd
DowntimeHours
RepairHours
FailureCause
FailureConsequence
RepairCost
IsRepeatFailure
```

### 2.4 `fact_Maintenance`

**Source filename:** None.

**Exists:** No.

`azure_machine_reliability_summary.csv` contains `maintenance_event_count`, but
that is an aggregate count, not a work-order fact table.

**Columns that need renaming:** None. No valid work-order source exists.

**Columns that need creating:** A complete work-order fact table must be created
from source maintenance records.

**Columns missing:**

```text
WorkOrderID
AssetID
MaintenanceDate
ActionID or ActionDescription
MaintenanceType
LaborHours
PartsCost
TotalCost
WorkOrderStatus
CompletionDate
```

### 2.5 `fact_PM_Compliance`

**Source filename:** None.

**Exists:** No.

No PM schedule, due date, completion date, team, status, or frequency file exists
in `data\processed`.

**Columns that need renaming:** None. No valid PM compliance source exists.

**Columns that need creating:** A complete PM compliance fact table must be
created from source PM records.

**Columns missing:**

```text
PMRecordID
AssetID
PMDueDate
PMCompletedDate
PMCategory
PMFrequency
AssignedTeam
CompletionStatus
ScheduleStatus
DaysOverdue
```

### 2.6 `dim_FailureMode`

**Source filename:** None.

**Exists:** No.

`azure_machine_reliability_summary.csv` has `last_failure_type`, but this is only
the latest observed failure type per asset and includes `None`. It is not a
complete failure-mode lookup.

**Columns that need renaming:** None.

**Columns that need creating:** If loaded, create a proper lookup with at least
`FailureModeID` and `FailureMode` from event-level failure data or an approved
lookup source.

**Columns missing:** `FailureModeID`, `FailureMode`

### 2.7 `dim_MaintenanceAction`

**Source filename:** None.

**Exists:** No.

No maintenance action lookup exists in `data\processed`.

**Columns that need renaming:** None.

**Columns that need creating:** If loaded, create a proper lookup with at least
`ActionID` and `ActionDescription` from maintenance work-order data or an
approved lookup source.

**Columns missing:** `ActionID`, `ActionDescription`

## 3. Required Column Check

### 3.1 `dim_Asset`

| Required field | Status | Source or issue |
|---|---|---|
| AssetID | Rename available | `lng_asset_id` |
| AssetName | Rename available | `lng_asset_name` |
| EquipmentCategory | Rename available | `lng_equipment_category` |
| CategoryGroup | Missing | Must be created or sourced |
| CriticalityRating | Missing | Must be created or sourced; `maintenance_priority` is not equivalent |
| Subsystem | Missing | Must be created or sourced |
| Location | Missing | Must be created or sourced |

### 3.2 `fact_Failure`

| Required field | Status | Source or issue |
|---|---|---|
| EventID | Missing | No event-level failure table |
| AssetID | Not valid for fact | `lng_asset_id` exists only at asset-summary grain |
| FailureDate | Missing | No failure date |
| FailureModeID or FailureMode | Partial but not valid | `last_failure_type` is last failure only, not event-level |
| DowntimeStart | Missing | No downtime start |
| DowntimeEnd | Missing | No downtime end |
| DowntimeHours | Partial but not valid | `estimated_downtime_hours` is asset-level summary |
| RepairHours | Partial but not valid | `mttr_style_hours` is asset-level summary |
| FailureCause | Missing | No event-level cause |
| FailureConsequence | Missing | No event-level consequence |
| RepairCost | Missing | No repair cost |
| IsRepeatFailure | Missing | No event-level repeat flag |

### 3.3 `fact_Maintenance`

| Required field | Status | Source or issue |
|---|---|---|
| WorkOrderID | Missing | No work-order table |
| AssetID | Missing | No work-order table |
| MaintenanceDate | Missing | No maintenance date |
| ActionID or ActionDescription | Missing | No maintenance action |
| MaintenanceType | Missing | No maintenance type |
| LaborHours | Missing | No labor hours |
| PartsCost | Missing | No parts cost |
| TotalCost | Missing | No total cost |
| WorkOrderStatus | Missing | No work-order status |
| CompletionDate | Missing | No completion date |

### 3.4 `fact_PM_Compliance`

| Required field | Status | Source or issue |
|---|---|---|
| PMRecordID | Missing | No PM compliance table |
| AssetID | Missing | No PM compliance table |
| PMDueDate | Missing | No due date |
| PMCompletedDate | Missing | No completion date |
| PMCategory | Missing | No PM category |
| PMFrequency | Missing | No PM frequency |
| AssignedTeam | Missing | No assigned team |
| CompletionStatus | Missing | No completion status |
| ScheduleStatus | Missing | No schedule status |
| DaysOverdue | Missing | Can be added in Power Query after PMDueDate and ScheduleStatus exist |

## 4. Data Quality Checks

### 4.1 `azure_machine_reliability_summary.csv`

| Check | Result |
|---|---|
| Duplicate primary keys | 0 duplicates for `machineID`; 0 duplicates for `lng_asset_id` |
| Blank primary keys | 0 blank `machineID`; 0 blank `lng_asset_id` |
| Null AssetID values | 0 null `lng_asset_id` values |
| Negative downtime | 0 negative `estimated_downtime_hours` values |
| Negative repair hours | 0 negative `mttr_style_hours` values; no `RepairHours` column exists |
| Invalid dates | Not testable; file has no date columns |
| Downtime end before downtime start | Not testable; file has no `DowntimeStart` or `DowntimeEnd` |
| Inconsistent asset IDs | 0 invalid values using expected `LNG-XXX-000` style pattern |
| Inconsistent equipment category names | 5 unique categories; no leading/trailing whitespace or casing variants detected |
| Inconsistent failure mode names | 5 `last_failure_type` values; no whitespace or casing variants detected |
| Unexpected text casing or whitespace | None detected in inspected category, model, failure type, and priority fields |
| PM completion dates before reasonable dates | Not applicable; no PM date columns |
| Overdue records without DaysOverdue | Not applicable; no PM records |
| Mixed data type columns | None detected |

Useful distinct values:

| Field | Distinct values |
|---|---|
| lng_equipment_category | Cooling Water Pumps; Electric Motors; Gas Compressors; Process Pumps; Utility Generators |
| last_failure_type | None; comp1; comp2; comp3; comp4 |
| maintenance_priority | Critical; Medium |

### 4.2 `phmsa_incident_risk_summary.csv`

| Check | Result |
|---|---|
| Duplicate primary keys | No primary key column exists; 0 exact duplicate rows detected |
| Blank primary keys | Not applicable; no primary key column exists |
| Null AssetID values | Not applicable; no AssetID column exists |
| Negative downtime | Not applicable; no downtime columns |
| Negative repair hours | Not applicable; no repair-hour columns |
| Invalid dates | `year` values are valid integers from 2010 through 2026 |
| Downtime end before downtime start | Not applicable; no downtime start/end columns |
| Inconsistent asset IDs | Not applicable; no AssetID column exists |
| Inconsistent equipment category names | Not applicable; no equipment category column |
| Inconsistent failure mode names | 8 cause categories; no whitespace or casing variants detected |
| Unexpected text casing or whitespace | No leading/trailing whitespace or casing variants detected in inspected text fields |
| PM completion dates before reasonable dates | Not applicable; no PM date columns |
| Overdue records without DaysOverdue | Not applicable; no PM records |
| Mixed data type columns | None detected |

Useful distinct values:

| Field | Distinct values |
|---|---|
| source_dataset | 2 |
| cause_category_if_available | 8 |
| incident_type_or_system_type_if_available | 22 |
| state_or_location_field_if_available | 47 |
| release_or_leak_field_if_available | 10 |

## 5. Relationship Readiness

| Relationship readiness check | Result |
|---|---|
| Every fact AssetID exists in dim_Asset | Cannot pass; no valid fact tables exist |
| Every FailureModeID exists in dim_FailureMode, if lookup exists | Cannot test; no `fact_Failure` and no `dim_FailureMode` lookup exist |
| Every ActionID exists in dim_MaintenanceAction, if lookup exists | Cannot test; no `fact_Maintenance` and no `dim_MaintenanceAction` lookup exist |
| Date columns suitable for dim_Date relationships | Not ready; required `FailureDate`, `MaintenanceDate`, and `PMDueDate` columns do not exist |

The current files do not support the six mandatory Power BI relationships:

```text
dim_Date[Date] -> fact_Failure[FailureDate]
dim_Asset[AssetID] -> fact_Failure[AssetID]
dim_Date[Date] -> fact_Maintenance[MaintenanceDate]
dim_Asset[AssetID] -> fact_Maintenance[AssetID]
dim_Date[Date] -> fact_PM_Compliance[PMDueDate]
dim_Asset[AssetID] -> fact_PM_Compliance[AssetID]
```

The two optional lookup relationships also cannot be validated yet:

```text
dim_FailureMode[FailureModeID] -> fact_Failure[FailureModeID]
dim_MaintenanceAction[ActionID] -> fact_Maintenance[ActionID]
```

## 6. Power BI Readiness Verdict

**Verdict:** Not ready - missing required tables.

Reason:
- `dim_Asset` can be partially created from `azure_machine_reliability_summary.csv`.
- `fact_Failure` is missing.
- `fact_Maintenance` is missing.
- `fact_PM_Compliance` is missing.
- Optional lookup tables are missing.
- The current CSVs are aggregate summaries, not transactional fact tables.

This is not a minor Power Query cleanup issue. Power Query can handle renaming,
data type conversion, trimming, and `DaysOverdue` calculation after the PM table
exists. It cannot recover event-level failure, work-order, or PM records from
the current aggregate summary files.

## 7. Exact Next Action

### First file to import into Power BI

After the missing fact tables exist, import the asset dimension first.

Current best candidate:

```text
data\processed\azure_machine_reliability_summary.csv
```

Use it as a staging query and transform it into `dim_Asset` by renaming:

```text
lng_asset_id -> AssetID
lng_asset_name -> AssetName
lng_equipment_category -> EquipmentCategory
```

Do not begin the full Power BI v0.2 build until the required fact tables are
available.

### Files that must be created before Power BI v0.2 build

Required:

```text
dim_Asset.csv or equivalent query output
fact_Failure.csv
fact_Maintenance.csv
fact_PM_Compliance.csv
```

Optional if source lookup data exists:

```text
dim_FailureMode.csv
dim_MaintenanceAction.csv
```

### Columns that must be added before Power BI

For `dim_Asset`:

```text
CategoryGroup
CriticalityRating
Subsystem
Location
```

For `fact_Failure`, create all required event-level fields:

```text
EventID
AssetID
FailureDate
FailureModeID or FailureMode
DowntimeStart
DowntimeEnd
DowntimeHours
RepairHours
FailureCause
FailureConsequence
RepairCost
IsRepeatFailure
```

For `fact_Maintenance`, create all required work-order fields:

```text
WorkOrderID
AssetID
MaintenanceDate
ActionID or ActionDescription
MaintenanceType
LaborHours
PartsCost
TotalCost
WorkOrderStatus
CompletionDate
```

For `fact_PM_Compliance`, create all required PM fields except `DaysOverdue` may
be created in Power Query after `PMDueDate` and `ScheduleStatus` exist:

```text
PMRecordID
AssetID
PMDueDate
PMCompletedDate
PMCategory
PMFrequency
AssignedTeam
CompletionStatus
ScheduleStatus
DaysOverdue
```

### Can Power Query handle the cleaning?

Power Query can handle:
- Column renaming for `dim_Asset`
- Data type conversion
- Text trimming and casing cleanup
- Removing duplicate asset rows if they appear later
- Creating `DaysOverdue` once `fact_PM_Compliance` exists
- Creating simple category grouping if an approved rule is documented

Power Query cannot safely create the missing event-level fact tables from the
current aggregate summaries.

### Is Python preprocessing required?

Yes, unless the missing fact-table CSVs already exist elsewhere.

A Python preprocessing step is required to produce the v0.2-ready star-schema
exports from raw/source data:

```text
dim_Asset
fact_Failure
fact_Maintenance
fact_PM_Compliance
```

The script must preserve real/adapted source lineage and must not generate
synthetic operational facts unless the portfolio explicitly labels them as
synthetic demonstration data.

## 8. Final Gate 0 Summary

| Item | Result |
|---|---|
| Files inspected | `azure_machine_reliability_summary.csv`; `phmsa_incident_risk_summary.csv` |
| Proposed Power BI tables | Partial `dim_Asset` only |
| Missing required data | `fact_Failure`, `fact_Maintenance`, `fact_PM_Compliance`; optional lookup files absent |
| Data quality blockers in existing files | No duplicate asset keys, no negative downtime, no mixed data types; blockers are schema/grain, not row cleanliness |
| Relationship readiness | Not ready; mandatory fact tables and date fields do not exist |
| Power BI v0.2 readiness | Not ready - missing required tables |

