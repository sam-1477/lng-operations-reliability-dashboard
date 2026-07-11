# Power BI v0.2 Data Validation Report

Validation date: 2026-07-11

## Row Counts

| Table | Rows | Columns |
|---|---:|---:|
| dim_asset.csv | 100 | 12 |
| fact_failure.csv | 761 | 15 |
| fact_maintenance.csv | 3286 | 13 |
| fact_pm_compliance.csv | 2640 | 12 |
| dim_failure_mode.csv | 10 | 6 |
| dim_maintenance_action.csv | 10 | 5 |

## Table Schemas

### dim_asset.csv

```text
AssetID
AssetName
EquipmentCategory
CategoryGroup
CriticalityRating
Subsystem
Location
Manufacturer
InstallDate
CurrentStatus
DataOrigin
IsIllustrative
```

### fact_failure.csv

```text
EventID
AssetID
FailureDate
FailureModeID
DowntimeStart
DowntimeEnd
DowntimeHours
RepairHours
FailureCause
FailureConsequence
RepairCost
ProductionLoss
IsRepeatFailure
DataOrigin
IsIllustrative
```

### fact_maintenance.csv

```text
WorkOrderID
AssetID
MaintenanceDate
ActionID
MaintenanceType
LaborHours
PartsCost
TotalCost
WorkOrderStatus
CompletionDate
PerformedBy
DataOrigin
IsIllustrative
```

### fact_pm_compliance.csv

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
DataOrigin
IsIllustrative
```

### dim_failure_mode.csv

```text
FailureModeID
FailureMode
FailureMechanism
FailureClass
TypicalRootCause
DataOrigin
```

### dim_maintenance_action.csv

```text
ActionID
ActionDescription
ActionType
ActionCategory
DataOrigin
```

## Validation Checks

| Check | Result | Detail |
|---|---|---|
| 1. All required files exist | PASS | all six required CSV files exist |
| 2. Exact required columns exist | PASS | all table schemas match the required column order |
| 3. Primary keys are unique | PASS | all primary keys are unique |
| 4. No blank primary keys | PASS | no blank primary keys |
| 5. No blank AssetID values in fact tables | PASS | fact AssetID columns are populated |
| 6. Every fact AssetID exists in dim_asset | PASS | all fact AssetIDs exist in dim_asset |
| 7. Every FailureModeID exists in dim_failure_mode | PASS | all fact_failure FailureModeID values exist in dim_failure_mode |
| 8. Every ActionID exists in dim_maintenance_action | PASS | all fact_maintenance ActionID values exist in dim_maintenance_action |
| 9. No negative downtime | PASS | no negative downtime |
| 10. No negative repair hours | PASS | no negative repair hours |
| 11. RepairHours <= DowntimeHours | PASS | RepairHours <= DowntimeHours |
| 12. DowntimeEnd >= DowntimeStart | PASS | DowntimeEnd >= DowntimeStart |
| 13. No negative labor hours or costs | PASS | no negative labor hours or costs |
| 14. CompletionDate >= MaintenanceDate | PASS | CompletionDate >= MaintenanceDate |
| 15. PM status consistency | PASS | PM completion and schedule statuses are internally consistent |
| 16. DaysOverdue consistency | PASS | DaysOverdue is positive only for Overdue PM records |
| 17. Valid date parsing | PASS | all required date columns parse successfully |
| 18. No mixed data types in required numeric columns | PASS | required numeric columns parse without mixed text values |
| 19. DataOrigin populated | PASS | DataOrigin populated in all six tables |
| 20. IsIllustrative populated where required | PASS | IsIllustrative populated and boolean where required |
| 21. Repeat-failure logic is reproducible | PASS | repeat-failure logic is reproducible |
| 22. Regeneration with same seed produces identical outputs | PASS | same seed regenerates byte-identical outputs |

## Field Provenance

### dim_asset.csv

| Field | Provenance |
|---|---|
| AssetID | Direct from existing Azure-to-LNG project mapping |
| AssetName | Direct from existing Azure-to-LNG project mapping |
| EquipmentCategory | Mapped from existing project category to LNG-style category |
| CategoryGroup | Derived from EquipmentCategory |
| CriticalityRating | Derived from source health score and category rule |
| Subsystem | Derived from source category |
| Location | Inferred deterministically from machineID |
| Manufacturer | Mapped from Azure machine model |
| InstallDate | Inferred from Azure machine age using reference year 2026 |
| CurrentStatus | Derived from source health score and priority |
| DataOrigin | Constant provenance label |
| IsIllustrative | Constant TRUE because the row is adapted for portfolio LNG-style use |

### fact_failure.csv

| Field | Provenance |
|---|---|
| EventID | Generated sequential key |
| AssetID | Mapped from Azure machineID using stable project mapping |
| FailureDate | Direct from Azure PdM failure timestamp |
| FailureModeID | Mapped from Azure failure code |
| DowntimeStart | Direct from Azure PdM failure timestamp |
| DowntimeEnd | Estimated as DowntimeStart plus DowntimeHours |
| DowntimeHours | Estimated fixed value by failure mode |
| RepairHours | Estimated as 80 percent of DowntimeHours |
| FailureCause | Mapped from failure-mode lookup |
| FailureConsequence | Derived from equipment category and downtime |
| RepairCost | Simulated deterministic lookup by category and failure mode |
| ProductionLoss | Estimated as DowntimeHours times category hourly loss rate |
| IsRepeatFailure | Derived from repeat event within 90 days |
| DataOrigin | Constant provenance label |
| IsIllustrative | Constant TRUE because row contains estimated/simulated operational values |

### fact_maintenance.csv

| Field | Provenance |
|---|---|
| WorkOrderID | Generated sequential key |
| AssetID | Mapped from Azure machineID using stable project mapping |
| MaintenanceDate | Direct from Azure PdM maintenance timestamp |
| ActionID | Mapped from Azure component code |
| MaintenanceType | Derived from failure and error proximity rules |
| LaborHours | Simulated deterministic lookup by action and maintenance type |
| PartsCost | Simulated deterministic lookup by action and category |
| TotalCost | Derived from LaborHours and PartsCost |
| WorkOrderStatus | Inferred as Completed because source events are historical |
| CompletionDate | Inferred from MaintenanceDate and action duration |
| PerformedBy | Simulated deterministic team assignment |
| DataOrigin | Constant provenance label |
| IsIllustrative | Constant TRUE because row contains simulated operational cost/team fields |

### fact_pm_compliance.csv

| Field | Provenance |
|---|---|
| PMRecordID | Generated sequential key |
| AssetID | Direct link to dim_asset AssetID |
| PMDueDate | Simulated deterministic schedule date |
| PMCompletedDate | Simulated deterministic completion date or blank |
| PMCategory | Mapped from equipment category and PM sequence |
| PMFrequency | Mapped from equipment category |
| AssignedTeam | Mapped from category and PM category |
| CompletionStatus | Simulated deterministic status |
| ScheduleStatus | Derived from due/completion date and project current date |
| DaysOverdue | Derived only when ScheduleStatus is Overdue |
| DataOrigin | Constant provenance label |
| IsIllustrative | Constant TRUE because PM schedule is simulated |

### dim_failure_mode.csv

| Field | Provenance |
|---|---|
| FailureModeID | Generated stable lookup key |
| FailureMode | Mapped engineering label |
| FailureMechanism | Inferred engineering label |
| FailureClass | Inferred engineering class |
| TypicalRootCause | Inferred engineering root cause |
| DataOrigin | Constant provenance label |

### dim_maintenance_action.csv

| Field | Provenance |
|---|---|
| ActionID | Generated stable lookup key |
| ActionDescription | Mapped engineering label |
| ActionType | Inferred engineering action type |
| ActionCategory | Inferred engineering action category |
| DataOrigin | Constant provenance label |

## Verdict

**Validation result:** PASS
