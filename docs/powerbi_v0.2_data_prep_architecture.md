# Power BI v0.2 Data Preparation Architecture
# ==========================================
# Gate 0 Remediation: Missing Table Generation Plan
# Date: 2026-07-11
# Repository: D:\ai-portfolio-projects\lng-reliability-dashboard

================================================================================
PART 1: REPOSITORY DATA INVENTORY
================================================================================

## 1.1 Available Public Datasets (data/raw/ extracted)

| Dataset | File | Rows | Key Columns |
|---------|------|------|-------------|
| Azure PdM Machines | PdM_machines.csv | 100 | machineID, model, age |
| Azure PdM Failures | PdM_failures.csv | 761 | datetime, machineID, failure |
| Azure PdM Maintenance | PdM_maint.csv | 3,286 | datetime, machineID, comp |
| Azure PdM Errors | PdM_errors.csv | 3,919 | datetime, machineID, errorID |
| Azure PdM Telemetry | PdM_telemetry.csv | 876,100 | machineID, volt, rotate, pressure, vibration |
| MetroPT-3 Compressor | MetroPT3_AirCompressor.csv | 1,516,948 | timestamp, TP2, TP3, H1, DV_pressure, Motor_current, etc. |
| PHMSA Gas Transmission | incident_gas_transmission...txt | ~2,000 | (pipe-delimited regulatory data) |
| PHMSA LNG Incidents | incident_liquefied_natural_gas...txt | ~100 | (pipe-delimited regulatory data) |

## 1.2 Existing Processed/Summary Outputs

| File | Rows | Granularity | Reusable For |
|------|------|-------------|--------------|
| azure_machine_reliability_summary.csv | 100 | Machine-level summary | dim_Asset (5 columns mappable) |
| phmsa_incident_risk_summary.csv | 1,564 | Year × Cause × State aggregates | Reference only (not fact tables) |

## 1.3 Existing Asset Register

Already present inside azure_machine_reliability_summary.csv:
- 100 machines mapped to LNG-style IDs
- 5 equipment categories (Process Pumps, Gas Compressors, Electric Motors, Utility Generators, Cooling Water Pumps)
- Each has: lng_asset_id, lng_asset_name, lng_equipment_category, machineID, model, age

## 1.4 Existing Failure Records

Raw event-level failures exist in PdM_failures.csv:
- 761 failure events across 100 machines
- Fields: datetime (YYYY-MM-DD HH:MM:SS), machineID, failure (comp1-comp4)
- Date range: 2015-01-05 to 2015-12-29
- This is the ONLY event-level failure source in the repository

## 1.5 Existing Maintenance Records

Raw event-level maintenance exists in PdM_maint.csv:
- 3,286 maintenance events across 100 machines
- Fields: datetime, machineID, comp (comp1-comp4)
- Date range: 2014-06-01 to 2015-12-31
- This is the ONLY event-level maintenance source

## 1.6 Existing Lookup Mappings

Azure failure types (comp1-comp4) already used in the summary. No formal failure-mode-to-mechanism mapping exists yet. The build script maps machines to LNG categories via a deterministic cycle.

## 1.7 Fields That Can Be Reused Directly

From azure_machine_reliability_summary.csv:
- lng_asset_id → AssetID
- lng_asset_name → AssetName
- lng_equipment_category → EquipmentCategory
- model → descriptive field
- age → install-date derivation

From PdM_failures.csv:
- datetime → FailureDate, DowntimeStart
- machineID → AssetID (via mapping)
- failure (comp1-comp4) → FailureModeID

From PdM_maint.csv:
- datetime → MaintenanceDate
- machineID → AssetID (via mapping)
- comp → ActionID

## 1.8 Fields Requiring Transformation

- AssetID: map machineID via the existing get_lng_asset_mapping() function
- FailureModeID: map comp1-comp4 to descriptive failure modes
- ActionID: map comp1-comp4 to maintenance action descriptions
- InstallDate: derive from age (2026 - age) as approximate year
- DowntimeHours: inferred, not real (see strategy below)
- RepairHours: inferred, not real
- RepairCost: simulated (see strategy below)
- ProductionLoss: simulated
- LaborHours / PartsCost / TotalCost: simulated

## 1.9 Fields Requiring Transparent Simulation

- CategoryGroup, CriticalityRating, Subsystem, Location, Manufacturer in dim_Asset
- RepairCost, ProductionLoss in fact_Failure
- LaborHours, PartsCost, TotalCost, PerformedBy in fact_Maintenance
- PM schedule entirely (fact_PM_Compliance) — no source PM data exists
- DowntimeEnd, DowntimeHours, RepairHours — no source downtime granularity
- FailureConsequence, IsRepeatFailure
- WorkOrderStatus
- CompletionStatus, ScheduleStatus, DaysOverdue, AssignedTeam


================================================================================
PART 2: TARGET TABLE SCHEMAS
================================================================================

## 2.1 dim_Asset

| Column | Type | Description |
|--------|------|-------------|
| AssetID | Text | PK — LNG-style ID (LNG-XXX-NNN) |
| AssetName | Text | Friendly name (e.g., "Gas Compressor 002") |
| EquipmentCategory | Text | Process Pumps, Gas Compressors, etc. |
| CategoryGroup | Text | Rotating, Electrical (derived from category) |
| CriticalityRating | Text | A/B/C (derived from health score) |
| Subsystem | Text | Production, Utility, Cooling (derived from category) |
| Location | Text | Train A / Train B / Utilities (derived from machineID parity) |
| Manufacturer | Text | Mapped from model (model1→Mfr A, model2→Mfr B, etc.) |
| InstallDate | Date | Derived: 2026 - age (YYYY-01-01) |
| CurrentStatus | Text | Operating / Under Review (from health score) |
| DataOrigin | Text | "Azure PdM (public) — adapted into LNG-style categories" |
| IsIllustrative | Boolean | TRUE (all 100 assets are adapted public data) |

## 2.2 fact_Failure

| Column | Type | Description |
|--------|------|-------------|
| EventID | Integer | PK — sequential 1..N |
| AssetID | Text | FK → dim_Asset (mapped from machineID) |
| FailureDate | Date | From PdM_failures.datetime |
| FailureModeID | Integer | FK → dim_FailureMode (mapped from comp1-comp4) |
| DowntimeStart | DateTime | Same as FailureDate 06:00:00 (when failure was recorded) |
| DowntimeEnd | DateTime | Estimated: DowntimeStart + DowntimeHours |
| DowntimeHours | Float | Estimated per failure mode (see strategy) |
| RepairHours | Float | Estimated = DowntimeHours * 0.8 |
| FailureCause | Text | Derived from failure mechanism lookup |
| FailureConsequence | Text | Low / Medium / High (derived from category) |
| RepairCost | Float | Simulated by equipment category (see $ table) |
| ProductionLoss | Float | Estimated: DowntimeHours * hourly loss rate |
| IsRepeatFailure | Boolean | TRUE if same AssetID+FailureModeID within 90 days |
| DataOrigin | Text | "Azure PdM (public) — event-level failures" |
| IsIllustrative | Boolean | TRUE for downtime/cost/production fields; FALSE for raw failure event |

## 2.3 fact_Maintenance

| Column | Type | Description |
|--------|------|-------------|
| WorkOrderID | Integer | PK — sequential 1..N |
| AssetID | Text | FK → dim_Asset (mapped from machineID) |
| MaintenanceDate | Date | From PdM_maint.datetime |
| ActionID | Integer | FK → dim_MaintenanceAction (mapped from comp1-comp4) |
| MaintenanceType | Text | Corrective / Preventive / Predictive / Condition-Based |
| LaborHours | Float | Simulated per action type |
| PartsCost | Float | Simulated per action type |
| TotalCost | Float | LaborHours * 150 + PartsCost |
| WorkOrderStatus | Text | Completed (all records have dates) |
| CompletionDate | Date | Same as MaintenanceDate (inferred) |
| PerformedBy | Text | Simulated crew assignment |
| DataOrigin | Text | "Azure PdM (public) — maintenance records adapted" |
| IsIllustrative | Boolean | TRUE for cost/labor fields; FALSE for raw maintenance events |

## 2.4 fact_PM_Compliance

| Column | Type | Description |
|--------|------|-------------|
| PMRecordID | Integer | PK — sequential 1..N |
| AssetID | Text | FK → dim_Asset |
| PMDueDate | Date | Generated per PM frequency schedule |
| PMCompletedDate | Date | PMDueDate ± random offset (deterministic seed) |
| PMCategory | Text | Inspection / Lubrication / Calibration / Overhaul |
| PMFrequency | Text | Monthly / Quarterly / Annually |
| AssignedTeam | Text | Mech / Elec / I&C |
| CompletionStatus | Text | Completed / Open / Cancelled |
| ScheduleStatus | Text | On Time / Completed Late / Overdue / Upcoming |
| DaysOverdue | Integer | max(0, PMCompletedDate - PMDueDate) when late |
| DataOrigin | Text | "Simulated PM schedule — based on LNG-style equipment PM intervals" |
| IsIllustrative | Boolean | TRUE (entirely simulated) |

## 2.5 dim_FailureMode

| Column | Type | Description |
|--------|------|-------------|
| FailureModeID | Integer | PK — 1..7 |
| FailureMode | Text | Bearing Failure, Seal Leak, Overheating, Vibration, Electrical Fault, Impeller Damage, Lubrication Failure |
| FailureMechanism | Text | Fatigue, Wear, Overload, Contamination, etc. |
| FailureClass | Text | Mechanical, Electrical, Process |
| TypicalRootCause | Text | Design, Manufacturing, Installation, Operation, Maintenance, Unknown |
| DataOrigin | Text | "Mapped from Azure PdM failure codes (comp1-comp4) with added LNG-style modes" |

## 2.6 dim_MaintenanceAction

| Column | Type | Description |
|--------|------|-------------|
| ActionID | Integer | PK — 1..8 |
| ActionDescription | Text | Replace bearing, Replace seal, Overhaul compressor, etc. |
| ActionType | Text | Corrective, Preventive, Predictive, Condition-Based |
| ActionCategory | Text | Mechanical, Electrical, Instrument, Lubrication, Inspection |
| DataOrigin | Text | "Mapped from Azure PdM component codes (comp1-comp4) with added LNG-style actions" |


================================================================================
PART 3: SOURCE-TO-TARGET MAPPING
================================================================================

## 3.1 dim_Asset — Source Mapping

| Target Column | Source | Transformation | Provenance |
|---------------|--------|----------------|------------|
| AssetID | summary.lng_asset_id | Direct copy | Direct |
| AssetName | summary.lng_asset_name | Direct copy | Direct |
| EquipmentCategory | summary.lng_equipment_category | Direct copy | Direct |
| CategoryGroup | Derived | Map: Pumps→Rotating, Compressors→Rotating, Motors→Electrical, Generators→Electrical | Derived |
| CriticalityRating | summary.asset_health_score | >=70→A, 40-69→B, <40→C | Derived |
| Subsystem | Derived | Pumps→Production, Compressors→Production, Motors→Production, Generators→Utility, Cooling Water Pumps→Cooling | Derived |
| Location | Derived | machineID % 3: 1→Train A, 2→Train B, 0→Utilities | Derived |
| Manufacturer | summary.model | model1→Siemens, model2→GE, model3→ABB, model4→Mitsubishi | Mapped |
| InstallDate | summary.age | 2026 - age → YYYY-01-01 | Inferred |
| CurrentStatus | summary.asset_health_score | <10→Under Review, else Operating | Derived |
| DataOrigin | Constant | "Azure PdM (public) — adapted into LNG-style categories" | Constant |
| IsIllustrative | Constant | TRUE | Constant |

## 3.2 fact_Failure — Source Mapping

| Target Column | Source | Transformation | Provenance |
|---------------|--------|----------------|------------|
| EventID | — | Sequential integer 1..761 | Generated |
| AssetID | failures.machineID | Map via get_lng_asset_mapping() | Direct |
| FailureDate | failures.datetime | Parse date only | Direct |
| FailureModeID | failures.failure | Map comp1→1, comp2→2, comp3→4, comp4→7 | Mapped |
| DowntimeStart | failures.datetime | Parse datetime | Direct |
| DowntimeEnd | failures.datetime + hours | DowntimeStart + pd.Timedelta(hours=DowntimeHours) | Estimated |
| DowntimeHours | failures.failure | comp1/comp2→8, comp3→16, comp4→24 (see table) | Estimated |
| RepairHours | DowntimeHours | DowntimeHours * 0.8 | Estimated |
| FailureCause | dim_FailureMode | Lookup via FailureModeID | Mapped |
| FailureConsequence | EquipmentCategory | Compressors→High, Pumps→High, Motors→Medium, Generators→Low, Cooling Water→Low | Derived |
| RepairCost | EquipmentCategory + FailureMode | See cost table (Section 5) | Simulated |
| ProductionLoss | DowntimeHours | DowntimeHours * hourly_rate (per category) | Estimated |
| IsRepeatFailure | Same AssetID+FailureModeID in 90d window | Computed via sort+shift | Derived |
| DataOrigin | Constant | "Azure PdM (public) — event-level failures" | Constant |
| IsIllustrative | Boolean | TRUE for Downtime/Repair/Cost/Production; FALSE for event & date | Computed |

Downtime hours per failure mode (from Azure PdM documentation conventions):
- comp1: 8 hours (minor repair)
- comp2: 8 hours (minor repair)
- comp3: 16 hours (moderate repair)
- comp4: 24 hours (major overhaul)

Hourly production loss rates:
- Gas Compressors: $5,000/hr
- Process Pumps: $3,000/hr
- Electric Motors: $2,000/hr
- Utility Generators: $1,500/hr
- Cooling Water Pumps: $1,000/hr

## 3.3 fact_Maintenance — Source Mapping

| Target Column | Source | Transformation | Provenance |
|---------------|--------|----------------|------------|
| WorkOrderID | — | Sequential integer 1..3286 | Generated |
| AssetID | maint.machineID | Map via get_lng_asset_mapping() | Direct |
| MaintenanceDate | maint.datetime | Parse date only | Direct |
| ActionID | maint.comp | Map comp1→1, comp2→2, comp3→4, comp4→6 | Mapped |
| MaintenanceType | maint.datetime vs failures | Corrective if failure within ±2 days; else Predictive (if errors nearby) else Preventive | Derived |
| LaborHours | ActionID | comp1→4, comp2→4, comp3→8, comp4→16 | Simulated |
| PartsCost | ActionID + EquipmentCategory | See cost table (Section 5) | Simulated |
| TotalCost | LaborHours + PartsCost | LaborHours * 150 + PartsCost | Computed |
| WorkOrderStatus | Constant | "Completed" (all raw rows have dates) | Inferred |
| CompletionDate | maint.datetime | Parse date only | Inferred |
| PerformedBy | machineID % 3 | 1→Internal Crew A, 2→Internal Crew B, 0→Contractor | Simulated |
| DataOrigin | Constant | "Azure PdM (public) — maintenance records adapted" | Constant |
| IsIllustrative | Boolean | TRUE for cost/labor/crew; FALSE for event & date | Computed |

Maintenance type classification logic:
1. Match each maintenance event to the nearest failure event on the same machine
2. If within ±2 days → "Corrective"
3. Else if error on same machine within ±7 days → "Predictive"
4. Else → "Preventive"

## 3.4 fact_PM_Compliance — Source Mapping

No source data exists. Entirely generated per the PM strategy (Section 7).

## 3.5 dim_FailureMode — Source Mapping

| Target Column | Source | Transformation | Provenance |
|---------------|--------|----------------|------------|
| FailureModeID | — | Integer 1..7 | Generated |
| FailureMode | Lookup map | See failure mode mapping table | Mapped |
| FailureMechanism | Lookup map | See failure mode mapping table | Inferred |
| FailureClass | Lookup map | See failure mode mapping table | Inferred |
| TypicalRootCause | Lookup map | See failure mode mapping table | Inferred |
| DataOrigin | Constant | "Mapped from Azure PdM failure codes — engineering domain knowledge" | Constant |

Failure Mode Mapping Table:

| ID | FailureMode | FailureMechanism | FailureClass | TypicalRootCause | Maps From |
|----|-------------|------------------|--------------|------------------|-----------|
| 1 | Bearing Failure | Fatigue/Wear | Mechanical | Maintenance | comp1 |
| 2 | Seal Leak | Wear/Contamination | Mechanical | Maintenance | comp2 |
| 3 | Overheating | Overload | Process | Operation | (extra) |
| 4 | Vibration | Fatigue | Mechanical | Design | comp3 |
| 5 | Electrical Fault | Contamination | Electrical | Manufacturing | (extra) |
| 6 | Impeller Damage | Erosion | Mechanical | Operation | (extra) |
| 7 | Lubrication Failure | Contamination | Process | Maintenance | comp4 |

## 3.6 dim_MaintenanceAction — Source Mapping

| Target Column | Source | Transformation | Provenance |
|---------------|--------|----------------|------------|
| ActionID | — | Integer 1..8 | Generated |
| ActionDescription | Lookup map | See action mapping table | Mapped |
| ActionType | Lookup map | See action mapping table | Inferred |
| ActionCategory | Lookup map | See action mapping table | Inferred |
| DataOrigin | Constant | "Mapped from Azure PdM component codes — engineering domain knowledge" | Constant |

Maintenance Action Mapping Table:

| ID | ActionDescription | ActionType | ActionCategory | Maps From |
|----|-------------------|------------|----------------|-----------|
| 1 | Replace bearing | Corrective | Mechanical | comp1 |
| 2 | Replace seal | Corrective | Mechanical | comp2 |
| 3 | Vibration analysis | Predictive | Mechanical | (extra) |
| 4 | Overhaul compressor stage | Corrective | Mechanical | comp3 |
| 5 | Oil analysis and change | Preventive | Lubrication | (extra) |
| 6 | Replace lubricant system component | Corrective | Lubrication | comp4 |
| 7 | Electrical insulation test | Preventive | Electrical | (extra) |
| 8 | Thermal imaging inspection | Condition-Based | Inspection | (extra) |

Note: comp1-comp4 are the Azure labels. Actions 3, 5, 7, 8 are extra LNG-style additions
that some PM records will reference.


================================================================================
PART 4: ASSET STRATEGY
================================================================================

## 4.1 Asset Register Design

The 100-machine Azure PdM dataset provides the foundation. Each machineID is mapped
via the existing get_lng_asset_mapping() function to produce:
- AssetID: LNG-{PREFIX}-{NNN}
- AssetName: {Category Name} {NNN}
- EquipmentCategory: one of 5 categories

Category cycle (machineID % 5):
0 → Cooling Water Pumps (CWP)
1 → Process Pumps (PMP)
2 → Gas Compressors (CMP)
3 → Electric Motors (MTR)
4 → Utility Generators (GEN)

## 4.2 Asset Attributes

| Attribute | Derivation | Example |
|-----------|-----------|---------|
| CategoryGroup | Rotating (Pumps, Compressors), Electrical (Motors, Generators) | Rotating |
| CriticalityRating | A: health >= 70, B: 40-69, C: < 40 | A |
| Subsystem | Pumps/Compressors→Production, Motors/Generators→Utility, CWP→Cooling | Production |
| Location | machineID % 3: 1→"Train A", 2→"Train B", 0→"Utilities" | Train A |
| Manufacturer | model1→Siemens, model2→GE, model3→ABB, model4→Mitsubishi | ABB |
| InstallDate | 2026 - age (approximate year, set to Jan 1) | 2018-01-01 |
| CurrentStatus | health < 10 → "Under Review", else "Operating" | Operating |
| DataOrigin | Fixed | "Azure PdM (public) — adapted into LNG-style categories" |
| IsIllustrative | TRUE | TRUE |

## 4.3 AssetID Stability

AssetIDs are deterministic — derived from machineID via a modulo-based hash function.
They are stable across regeneration. All fact tables reference these same AssetIDs
via the same mapping function (get_lng_asset_mapping()).


================================================================================
PART 5: FAILURE EVENT STRATEGY
================================================================================

## 5.1 Event Granularity

One row per raw failure event in PdM_failures.csv (761 events).

## 5.2 Failure Date Derivation

Directly from PdM_failures.datetime. All events are in 2015 (Jan-Dec). These are real
public dataset timestamps.

## 5.3 MachineID to AssetID Mapping

Identical to the function used in build_azure_reliability_summary.py:
get_lng_asset_mapping(machine_id) → lng_asset_id

## 5.4 Failure Mode Mapping

Azure failure codes → descriptive failure modes:
- comp1 → Bearing Failure (ID=1)
- comp2 → Seal Leak (ID=2)
- comp3 → Vibration (ID=4)
- comp4 → Lubrication Failure (ID=7)

## 5.5 Downtime Assumptions (REPRODUCIBLE)

Per-failure-mode fixed downtime hours (not random):
- comp1 → 8 hours
- comp2 → 8 hours
- comp3 → 16 hours
- comp4 → 24 hours

These are conservative fixed estimates based on typical repair scope. Not random.

## 5.6 Repair-Hour Assumptions

RepairHours = DowntimeHours * 0.8
Rationale: 20% of downtime is logistics/waiting, 80% is active repair.

## 5.7 Cost Assumptions (DETERMINISTIC SIMULATION)

Base repair costs per failure mode + equipment category:

| FailureModeID | Compressors | Pumps | Motors | Generators | Cooling Water |
|---------------|-------------|-------|--------|------------|---------------|
| 1 (Bearing) | $12,000 | $8,000 | $6,000 | $10,000 | $5,000 |
| 2 (Seal Leak) | $8,000 | $5,000 | $4,000 | $6,000 | $4,000 |
| 4 (Vibration) | $20,000 | $12,000 | $10,000 | $15,000 | $8,000 |
| 7 (Lubrication) | $15,000 | $10,000 | $8,000 | $12,000 | $7,000 |

These are illustrative portfolio costs, NOT real LNG plant repair costs.

ProductionLoss = DowntimeHours * hourly_rate (from Section 3.2)

## 5.8 Consequence Classification

| Equipment Category | Failure Consequence |
|--------------------|---------------------|
| Gas Compressors | High |
| Process Pumps | High |
| Electric Motors | Medium |
| Utility Generators | Low |
| Cooling Water Pumps | Low |

## 5.9 Repeat-Failure Logic

IsRepeatFailure = TRUE if:
- Same AssetID
- Same FailureModeID
- FailureDate within 90 days of a previous failure
Computed by sorting by AssetID + FailureDate, checking previous row.

## 5.10 DataOrigin and IsIllustrative

- DataOrigin: "Azure PdM (public) — event-level failures"
- IsIllustrative: TRUE for DowntimeHours, DowntimeEnd, RepairHours, RepairCost, ProductionLoss
- IsIllustrative: FALSE for EventID, AssetID, FailureDate, FailureModeID (real events)
- Note: The raw Azure PdM failure events ARE real public data. Only the LNG-specific
  fields (costs, downtime hours, consequences) are estimated/illustrative.


================================================================================
PART 6: MAINTENANCE WORK-ORDER STRATEGY
================================================================================

## 6.1 Record Source

Raw PdM_maint.csv provides 3,286 maintenance events. Each has datetime, machineID, and comp.

## 6.2 Maintenance Type Classification

For each maintenance record:
1. Find the nearest failure event (same machineID, PdM_failures.csv)
2. If failure exists within ±2 days → "Corrective"
3. Else, check errors (PdM_errors.csv) — if error on same machine within ±7 days → "Predictive"
4. Else → "Preventive"

No "Condition-Based" records will appear in the primary source mapping, but some simulated
PM records may reference CBM action types.

## 6.3 Action Mapping

Azure comp → ActionID:
- comp1 → 1 (Replace bearing)
- comp2 → 2 (Replace seal)
- comp3 → 4 (Overhaul compressor stage)
- comp4 → 6 (Replace lubricant system component)

## 6.4 Labor and Cost Values (DETERMINISTIC)

| ActionID | LaborHours | PartsCost Base |
|----------|-----------|----------------|
| 1 (Replace bearing) | 4 | $5,000 |
| 2 (Replace seal) | 4 | $3,000 |
| 4 (Overhaul compressor) | 8 | $12,000 |
| 6 (Replace lube component) | 8 | $8,000 |

PartsCost is the base value. TotalCost = LaborHours * 150 + PartsCost.
Compressor category gets 1.5x parts multiplier (higher spec parts).

## 6.5 Work-Order Status

All raw maintenance records from Azure PdM have timestamps in the past, so:
- WorkOrderStatus = "Completed"
- CompletionDate = MaintenanceDate (inferred — no separate completion date exists)

## 6.6 Crew Assignment (DETERMINISTIC SEED)

PerformedBy based on machineID % 3:
- 1 → "Internal Crew A"
- 2 → "Internal Crew B"
- 0 → "Contractor — Rotating Equipment Specialist"


================================================================================
PART 7: PM COMPLIANCE STRATEGY
================================================================================

## 7.1 PM Schedule Generation

Entirely simulated. No source PM data exists. All PM compliance records are labeled
IsIllustrative=TRUE and DataOrigin="Simulated PM schedule...".

## 7.2 PM Frequencies by Equipment Category

| Equipment Category | PM Frequency | PM Categories |
|--------------------|--------------|---------------|
| Gas Compressors | Monthly | Inspection, Lubrication, Vibration Analysis |
| Process Pumps | Monthly | Inspection, Lubrication |
| Electric Motors | Quarterly | Inspection, Electrical Test |
| Utility Generators | Quarterly | Inspection, Electrical Test |
| Cooling Water Pumps | Monthly | Inspection, Lubrication |

## 7.3 Schedule Period

PM window: 2020-01-01 to 2025-12-31 (6 years × 12-4 cycles per asset per year)

This provides approximately:
- 100 assets × 6 years × avg 8 PM/year ≈ 4,800 PM records

## 7.4 Due-Date Generation (DETERMINISTIC SEED)

For each asset:
1. Base start date: max(InstallDate + 30 days, 2020-01-01)
2. Generate due dates at the frequency interval
3. Random seed: hash(AssetID) for reproducible date offsets

## 7.5 Completion-Date Rules (DETERMINISTIC SEED)

For each PM record:
1. 70%: completed on time (PMCompletedDate = PMDueDate - random(0, 3) days)
2. 15%: completed late (PMCompletedDate = PMDueDate + random(1, 14) days)
3. 10%: overdue / not completed (PMCompletedDate = NULL, ScheduleStatus = "Overdue")
4. 5%: cancelled (CompletionStatus = "Cancelled")

Random seed: hash(AssetID + PMDueDate) ensures deterministic regeneration.

## 7.6 Status Logic

CompletionStatus:
- PMCompletedDate not null → "Completed"
- PMCompletedDate null AND PMDueDate in future → "Open"
- PMCompletedDate null AND explicitly cancelled → "Cancelled"

ScheduleStatus:
- Completed AND PMCompletedDate <= PMDueDate → "On Time"
- Completed AND PMCompletedDate > PMDueDate → "Completed Late"
- NOT completed AND PMDueDate < today → "Overdue"
- NOT completed AND PMDueDate >= today → "Upcoming"

DaysOverdue:
- IF ScheduleStatus = "Overdue": (PMDueDate - today).days (positive)
- IF ScheduleStatus = "Completed Late": (PMCompletedDate - PMDueDate).days
- ELSE: NULL

## 7.7 Assigned Teams

| Equipment Category | Default Team |
|--------------------|--------------|
| Gas Compressors | Mech |
| Process Pumps | Mech |
| Electric Motors | Elec |
| Utility Generators | Elec |
| Cooling Water Pumps | Mech |

Some variation: 10% of records get "I&C" team for calibration/instrument PMs.

## 7.8 Illustrative-Data Labeling

All PM records: DataOrigin = "Simulated PM schedule — based on LNG-style equipment PM intervals"
All PM records: IsIllustrative = TRUE


================================================================================
PART 8: VALIDATION RULES
================================================================================

## 8.1 Primary Key Uniqueness

| Table | PK Column | Check |
|-------|-----------|-------|
| dim_Asset | AssetID | assert df['AssetID'].is_unique |
| fact_Failure | EventID | assert df['EventID'].is_unique |
| fact_Maintenance | WorkOrderID | assert df['WorkOrderID'].is_unique |
| fact_PM_Compliance | PMRecordID | assert df['PMRecordID'].is_unique |
| dim_FailureMode | FailureModeID | assert df['FailureModeID'].is_unique |
| dim_MaintenanceAction | ActionID | assert df['ActionID'].is_unique |

## 8.2 No Blank Primary Keys

For each PK column: assert not df[pk_col].isna().any()

## 8.3 Referential Integrity

- All fact_Failure.AssetID exist in dim_Asset.AssetID
- All fact_Maintenance.AssetID exist in dim_Asset.AssetID
- All fact_PM_Compliance.AssetID exist in dim_Asset.AssetID
- All fact_Failure.FailureModeID exist in dim_FailureMode.FailureModeID
- All fact_Maintenance.ActionID exist in dim_MaintenanceAction.ActionID

## 8.4 No Negative Values

Check columns:
- fact_Failure: DowntimeHours >= 0, RepairHours >= 0, RepairCost >= 0, ProductionLoss >= 0
- fact_Maintenance: LaborHours >= 0, PartsCost >= 0, TotalCost >= 0
- fact_PM_Compliance: DaysOverdue >= 0 where not null

## 8.5 Date Consistency

- fact_Failure: DowntimeEnd >= DowntimeStart
- fact_Maintenance: CompletionDate >= MaintenanceDate
- fact_PM_Compliance: PMCompletedDate is null OR PMCompletedDate >= PMDueDate - 7 days (allow early completion up to 1 week)

## 8.6 Status Consistency

- fact_PM_Compliance: CompletionStatus="Completed" → PMCompletedDate not null
- fact_PM_Compliance: CompletionStatus="Cancelled" → PMCompletedDate is null
- fact_PM_Compliance: DaysOverdue is null when ScheduleStatus in ("On Time", "Upcoming")
- fact_PM_Compliance: DaysOverdue >= 0 when ScheduleStatus in ("Overdue", "Completed Late")

## 8.7 Date Ranges

- All dates: 2010-01-01 to 2026-12-31 (project scope)
- InstallDate: 1990-01-01 to 2026-12-31

## 8.8 No Mixed Data Types

- Integer columns: assert dtype is int64
- Float columns: assert dtype is float64
- String columns: assert dtype is object
- Date columns: assert dtype is datetime64
- Boolean columns: assert dtype is bool

## 8.9 Provenance Fields

- All six tables MUST have DataOrigin populated (no nulls, no blanks)
- All six tables MUST have IsIllustrative populated (no nulls)
- IsIllustrative must be boolean True or False only

## 8.10 Reproducibility

- Build script uses fixed random seed: 42
- All hash-based determinations use hash() on deterministic strings
- Re-running build_powerbi_v02_data.py MUST produce identical output


================================================================================
PART 9: OUTPUT SCRIPTS
================================================================================

## 9.1 Build Script: scripts/build_powerbi_v02_data.py

Phases:
1. Read raw Azure PdM files + existing processed summary
2. Build dim_Asset from summary + derived columns
3. Build dim_FailureMode (hardcoded lookup)
4. Build dim_MaintenanceAction (hardcoded lookup)
5. Build fact_Failure from PdM_failures.csv + mappings
6. Build fact_Maintenance from PdM_maint.csv + type classification
7. Build fact_PM_Compliance (simulated schedule)
8. Write all 6 CSVs to data/processed/
9. Print summary: row counts, schema preview

## 9.2 Validation Script: scripts/validate_powerbi_v02_data.py

Checks:
1. All 6 CSVs exist and are readable
2. PK uniqueness (8.1)
3. No blank PKs (8.2)
4. Referential integrity (8.3)
5. No negative values (8.4)
6. Date consistency (8.5)
7. Status consistency (8.6)
8. Date ranges (8.7)
9. Data types (8.8)
10. Provenance fields (8.9)
11. Write report: docs/powerbi_v0.2_data_validation_report.md
12. Exit code 0 on pass, 1 on any failure

Prints clear pass/fail for each check with detail.


================================================================================
PART 10: CODEX HANDOFF
================================================================================

See the prompt below labelled "PASTE INTO CODEX CLI".


================================================================================
APPENDIX A: FIELD PROVENANCE LEGEND
================================================================================

| Label | Meaning |
|-------|---------|
| Direct | Copied without transformation from a real public dataset column |
| Derived | Computed via deterministic rule from real public data |
| Mapped | Converted via a lookup table (Azure code → LNG label) |
| Inferred | Estimated from available data using reasonable assumptions |
| Estimated | Approximated using engineering domain knowledge (documented basis) |
| Simulated | Generated values — no real source data (documented with seed) |
| Generated | Sequential key or identifier — no data lineage |
| Constant | Fixed string, not data-derived |

================================================================================
APPENDIX B: SIMULATED FIELD DISCLOSURE TABLE
================================================================================

| Table | Field | Simulation Method | Seed |
|-------|-------|-------------------|------|
| dim_Asset | CriticalityRating | Derived from health score | — |
| dim_Asset | Subsystem | Derived from category | — |
| dim_Asset | Location | Derived from machineID parity | — |
| dim_Asset | Manufacturer | Mapped from model | — |
| dim_Asset | InstallDate | Derived from age | — |
| fact_Failure | DowntimeHours | Fixed per failure mode | — |
| fact_Failure | DowntimeEnd | Computed from DowntimeStart + DowntimeHours | — |
| fact_Failure | RepairHours | DowntimeHours * 0.8 | — |
| fact_Failure | FailureConsequence | Derived from category | — |
| fact_Failure | RepairCost | Per-mode × per-category lookup table | — |
| fact_Failure | ProductionLoss | DowntimeHours × hourly rate table | — |
| fact_Maintenance | MaintenanceType | Classified from failure/error proximity | — |
| fact_Maintenance | LaborHours | Fixed per action | — |
| fact_Maintenance | PartsCost | Per-action lookup table | — |
| fact_Maintenance | TotalCost | Computed formula | — |
| fact_Maintenance | PerformedBy | machineID % 3 | — |
| fact_PM_Compliance | ALL FIELDS | Entirely simulated | hash(AssetID + date), seed 42 |
| dim_FailureMode | FailureMechanism | Engineering domain knowledge | — |
| dim_FailureMode | FailureClass | Engineering domain knowledge | — |
| dim_FailureMode | TypicalRootCause | Engineering domain knowledge | — |
| dim_MaintenanceAction | ActionType | Engineering domain knowledge | — |
| dim_MaintenanceAction | ActionCategory | Engineering domain knowledge | — |