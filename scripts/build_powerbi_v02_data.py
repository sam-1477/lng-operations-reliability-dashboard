"""Build Power BI v0.2 star-schema CSV files.

The pipeline uses public Azure Predictive Maintenance event-level data where it
exists, and clearly labels adapted, estimated, and simulated fields. It does not
modify raw data and does not create or edit a PBIX file.

Run from the project root:
    python scripts\\build_powerbi_v02_data.py
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date, datetime
from pathlib import Path
from tempfile import TemporaryDirectory
from typing import Iterable

import hashlib
import random

try:
    import pandas as pd
except ImportError as error:  # pragma: no cover - runtime dependency guard
    raise SystemExit(
        "This script requires pandas. Install project dependencies first."
    ) from error


PROJECT_ROOT = Path(__file__).resolve().parents[1]
AZURE_RAW_DIR = PROJECT_ROOT / "data" / "raw" / "extracted" / "azure_pdm"
PROCESSED_DIR = PROJECT_ROOT / "data" / "processed"

MACHINES_FILE = AZURE_RAW_DIR / "PdM_machines.csv"
FAILURES_FILE = AZURE_RAW_DIR / "PdM_failures.csv"
MAINT_FILE = AZURE_RAW_DIR / "PdM_maint.csv"
ERRORS_FILE = AZURE_RAW_DIR / "PdM_errors.csv"
SUMMARY_FILE = PROCESSED_DIR / "azure_machine_reliability_summary.csv"

RANDOM_SEED = 42
REFERENCE_YEAR = 2026
PROJECT_CURRENT_DATE = date(2026, 7, 11)

OUTPUT_FILES = {
    "dim_asset": "dim_asset.csv",
    "fact_failure": "fact_failure.csv",
    "fact_maintenance": "fact_maintenance.csv",
    "fact_pm_compliance": "fact_pm_compliance.csv",
    "dim_failure_mode": "dim_failure_mode.csv",
    "dim_maintenance_action": "dim_maintenance_action.csv",
}

DIM_ASSET_COLUMNS = [
    "AssetID",
    "AssetName",
    "EquipmentCategory",
    "CategoryGroup",
    "CriticalityRating",
    "Subsystem",
    "Location",
    "Manufacturer",
    "InstallDate",
    "CurrentStatus",
    "DataOrigin",
    "IsIllustrative",
]

FACT_FAILURE_COLUMNS = [
    "EventID",
    "AssetID",
    "FailureDate",
    "FailureModeID",
    "DowntimeStart",
    "DowntimeEnd",
    "DowntimeHours",
    "RepairHours",
    "FailureCause",
    "FailureConsequence",
    "RepairCost",
    "ProductionLoss",
    "IsRepeatFailure",
    "DataOrigin",
    "IsIllustrative",
]

FACT_MAINTENANCE_COLUMNS = [
    "WorkOrderID",
    "AssetID",
    "MaintenanceDate",
    "ActionID",
    "MaintenanceType",
    "LaborHours",
    "PartsCost",
    "TotalCost",
    "WorkOrderStatus",
    "CompletionDate",
    "PerformedBy",
    "DataOrigin",
    "IsIllustrative",
]

FACT_PM_COLUMNS = [
    "PMRecordID",
    "AssetID",
    "PMDueDate",
    "PMCompletedDate",
    "PMCategory",
    "PMFrequency",
    "AssignedTeam",
    "CompletionStatus",
    "ScheduleStatus",
    "DaysOverdue",
    "DataOrigin",
    "IsIllustrative",
]

DIM_FAILURE_MODE_COLUMNS = [
    "FailureModeID",
    "FailureMode",
    "FailureMechanism",
    "FailureClass",
    "TypicalRootCause",
    "DataOrigin",
]

DIM_MAINTENANCE_ACTION_COLUMNS = [
    "ActionID",
    "ActionDescription",
    "ActionType",
    "ActionCategory",
    "DataOrigin",
]

DATA_ORIGIN_ASSET = (
    "Direct/Mapped/Derived/Inferred from public Azure PdM; illustrative LNG-style "
    "asset register"
)
DATA_ORIGIN_FAILURE = (
    "Direct/Mapped/Derived/Estimated/Simulated from public Azure PdM event-level "
    "failures"
)
DATA_ORIGIN_MAINTENANCE = (
    "Direct/Mapped/Derived/Inferred/Simulated from public Azure PdM maintenance "
    "events"
)
DATA_ORIGIN_PM = (
    "Simulated/Generated scheduled maintenance dataset; seed=42; no real operator "
    "PM data"
)
DATA_ORIGIN_FAILURE_MODE = (
    "Generated/Mapped/Inferred lookup from Azure PdM failure codes and engineering "
    "labels"
)
DATA_ORIGIN_ACTION = (
    "Generated/Mapped/Inferred lookup from Azure PdM component codes and "
    "engineering labels"
)

FIELD_PROVENANCE = {
    "dim_asset": {
        "AssetID": "Direct from existing Azure-to-LNG project mapping",
        "AssetName": "Direct from existing Azure-to-LNG project mapping",
        "EquipmentCategory": "Mapped from existing project category to LNG-style category",
        "CategoryGroup": "Derived from EquipmentCategory",
        "CriticalityRating": "Derived from source health score and category rule",
        "Subsystem": "Derived from source category",
        "Location": "Inferred deterministically from machineID",
        "Manufacturer": "Mapped from Azure machine model",
        "InstallDate": "Inferred from Azure machine age using reference year 2026",
        "CurrentStatus": "Derived from source health score and priority",
        "DataOrigin": "Constant provenance label",
        "IsIllustrative": "Constant TRUE because the row is adapted for portfolio LNG-style use",
    },
    "fact_failure": {
        "EventID": "Generated sequential key",
        "AssetID": "Mapped from Azure machineID using stable project mapping",
        "FailureDate": "Direct from Azure PdM failure timestamp",
        "FailureModeID": "Mapped from Azure failure code",
        "DowntimeStart": "Direct from Azure PdM failure timestamp",
        "DowntimeEnd": "Estimated as DowntimeStart plus DowntimeHours",
        "DowntimeHours": "Estimated fixed value by failure mode",
        "RepairHours": "Estimated as 80 percent of DowntimeHours",
        "FailureCause": "Mapped from failure-mode lookup",
        "FailureConsequence": "Derived from equipment category and downtime",
        "RepairCost": "Simulated deterministic lookup by category and failure mode",
        "ProductionLoss": "Estimated as DowntimeHours times category hourly loss rate",
        "IsRepeatFailure": "Derived from repeat event within 90 days",
        "DataOrigin": "Constant provenance label",
        "IsIllustrative": "Constant TRUE because row contains estimated/simulated operational values",
    },
    "fact_maintenance": {
        "WorkOrderID": "Generated sequential key",
        "AssetID": "Mapped from Azure machineID using stable project mapping",
        "MaintenanceDate": "Direct from Azure PdM maintenance timestamp",
        "ActionID": "Mapped from Azure component code",
        "MaintenanceType": "Derived from failure and error proximity rules",
        "LaborHours": "Simulated deterministic lookup by action and maintenance type",
        "PartsCost": "Simulated deterministic lookup by action and category",
        "TotalCost": "Derived from LaborHours and PartsCost",
        "WorkOrderStatus": "Inferred as Completed because source events are historical",
        "CompletionDate": "Inferred from MaintenanceDate and action duration",
        "PerformedBy": "Simulated deterministic team assignment",
        "DataOrigin": "Constant provenance label",
        "IsIllustrative": "Constant TRUE because row contains simulated operational cost/team fields",
    },
    "fact_pm_compliance": {
        "PMRecordID": "Generated sequential key",
        "AssetID": "Direct link to dim_asset AssetID",
        "PMDueDate": "Simulated deterministic schedule date",
        "PMCompletedDate": "Simulated deterministic completion date or blank",
        "PMCategory": "Mapped from equipment category and PM sequence",
        "PMFrequency": "Mapped from equipment category",
        "AssignedTeam": "Mapped from category and PM category",
        "CompletionStatus": "Simulated deterministic status",
        "ScheduleStatus": "Derived from due/completion date and project current date",
        "DaysOverdue": "Derived only when ScheduleStatus is Overdue",
        "DataOrigin": "Constant provenance label",
        "IsIllustrative": "Constant TRUE because PM schedule is simulated",
    },
    "dim_failure_mode": {
        "FailureModeID": "Generated stable lookup key",
        "FailureMode": "Mapped engineering label",
        "FailureMechanism": "Inferred engineering label",
        "FailureClass": "Inferred engineering class",
        "TypicalRootCause": "Inferred engineering root cause",
        "DataOrigin": "Constant provenance label",
    },
    "dim_maintenance_action": {
        "ActionID": "Generated stable lookup key",
        "ActionDescription": "Mapped engineering label",
        "ActionType": "Inferred engineering action type",
        "ActionCategory": "Inferred engineering action category",
        "DataOrigin": "Constant provenance label",
    },
}


def stable_int(value: str) -> int:
    """Return a deterministic integer for a string across Python processes."""
    digest = hashlib.sha256(value.encode("utf-8")).hexdigest()
    return int(digest[:16], 16)


def stable_rng(value: str) -> random.Random:
    """Return a deterministic RNG seeded from the fixed seed and a value."""
    return random.Random(RANDOM_SEED + stable_int(value))


def add_months(input_date: date, months: int) -> date:
    """Add whole months while preserving a valid day-of-month."""
    year = input_date.year + (input_date.month - 1 + months) // 12
    month = (input_date.month - 1 + months) % 12 + 1
    day = min(input_date.day, days_in_month(year, month))
    return date(year, month, day)


def days_in_month(year: int, month: int) -> int:
    """Return the number of days in a month."""
    if month == 12:
        next_month = date(year + 1, 1, 1)
    else:
        next_month = date(year, month + 1, 1)
    return (next_month - date(year, month, 1)).days


def check_required_sources() -> None:
    """Stop with a clear message when required source files are missing."""
    required = [MACHINES_FILE, FAILURES_FILE, MAINT_FILE, ERRORS_FILE, SUMMARY_FILE]
    missing = [path for path in required if not path.exists()]
    if not missing:
        return

    lines = ["Missing required source files:"]
    lines.extend(f"- {path.relative_to(PROJECT_ROOT)}" for path in missing)
    raise SystemExit("\n".join(lines))


def read_sources() -> dict[str, pd.DataFrame]:
    """Read all source CSV files used by the build."""
    check_required_sources()
    sources = {
        "machines": pd.read_csv(MACHINES_FILE),
        "failures": pd.read_csv(FAILURES_FILE),
        "maintenance": pd.read_csv(MAINT_FILE),
        "errors": pd.read_csv(ERRORS_FILE),
        "summary": pd.read_csv(SUMMARY_FILE),
    }
    for name in ("failures", "maintenance", "errors"):
        sources[name]["datetime"] = pd.to_datetime(sources[name]["datetime"])
    return sources


def normalize_source_category(source_category: str) -> str:
    """Map existing project categories into compact LNG-style categories."""
    mapping = {
        "Gas Compressors": "Compressor",
        "Process Pumps": "Pump",
        "Cooling Water Pumps": "Pump",
        "Electric Motors": "Electrical",
        "Utility Generators": "Generator",
    }
    return mapping.get(source_category, "Other")


def category_group(equipment_category: str) -> str:
    mapping = {
        "Compressor": "Rotating Equipment",
        "Pump": "Rotating Equipment",
        "Gas Turbine": "Rotating Equipment",
        "Generator": "Power Generation",
        "Heat Exchanger": "Static Equipment",
        "Pipeline": "Pipeline",
        "Storage": "Storage",
        "Electrical": "Electrical",
        "Instrumentation": "Instrumentation",
    }
    return mapping.get(equipment_category, "Other")


def subsystem(source_category: str, equipment_category: str) -> str:
    if source_category == "Cooling Water Pumps":
        return "Utilities - Cooling Water"
    if equipment_category == "Compressor":
        return "Gas Compression"
    if equipment_category == "Pump":
        return "Liquefaction Support"
    if equipment_category == "Generator":
        return "Power Generation"
    if equipment_category == "Electrical":
        return "Electrical Distribution"
    return "General Utilities"


def location_for_machine(machine_id: int, equipment_category: str) -> str:
    if equipment_category in {"Generator", "Electrical"}:
        return "Utilities"
    remainder = machine_id % 3
    if remainder == 1:
        return "Train 1"
    if remainder == 2:
        return "Train 2"
    return "Common Area"


def manufacturer(model: str) -> str:
    mapping = {
        "model1": "Siemens Energy",
        "model2": "GE Vernova",
        "model3": "ABB",
        "model4": "Mitsubishi Heavy Industries",
    }
    return mapping.get(model, "Mapped Manufacturer")


def criticality(row: pd.Series, equipment_category: str) -> str:
    health = float(row.get("asset_health_score", 100.0))
    priority = str(row.get("maintenance_priority", "")).strip()
    if equipment_category in {"Compressor", "Generator"} and health < 65:
        return "A"
    if priority == "Critical" or health < 40:
        return "A"
    if priority in {"High", "Medium"} or health < 75:
        return "B"
    return "C"


def build_dim_asset(sources: dict[str, pd.DataFrame]) -> pd.DataFrame:
    """Build the Power BI asset dimension from existing Azure project mapping."""
    summary = sources["summary"].copy()
    rows: list[dict] = []

    for _, row in summary.sort_values("machineID").iterrows():
        machine_id = int(row["machineID"])
        source_category = str(row["lng_equipment_category"])
        equipment_category = normalize_source_category(source_category)
        install_year = REFERENCE_YEAR - int(row["age"])
        health = float(row.get("asset_health_score", 100.0))
        priority = str(row.get("maintenance_priority", "")).strip()

        rows.append(
            {
                "AssetID": row["lng_asset_id"],
                "AssetName": row["lng_asset_name"],
                "EquipmentCategory": equipment_category,
                "CategoryGroup": category_group(equipment_category),
                "CriticalityRating": criticality(row, equipment_category),
                "Subsystem": subsystem(source_category, equipment_category),
                "Location": location_for_machine(machine_id, equipment_category),
                "Manufacturer": manufacturer(str(row["model"])),
                "InstallDate": date(install_year, 1, 1).isoformat(),
                "CurrentStatus": "Under Review"
                if health < 20 or priority == "Critical"
                else "Operating",
                "DataOrigin": DATA_ORIGIN_ASSET,
                "IsIllustrative": True,
            }
        )

    return pd.DataFrame(rows, columns=DIM_ASSET_COLUMNS)


def build_machine_asset_map(sources: dict[str, pd.DataFrame]) -> pd.DataFrame:
    """Return machineID to asset metadata used by fact builders."""
    summary = sources["summary"].copy()
    summary["EquipmentCategory"] = summary["lng_equipment_category"].apply(
        normalize_source_category
    )
    return summary[
        [
            "machineID",
            "lng_asset_id",
            "lng_asset_name",
            "lng_equipment_category",
            "EquipmentCategory",
        ]
    ].rename(columns={"lng_asset_id": "AssetID"})


def build_dim_failure_mode() -> pd.DataFrame:
    """Build stable failure-mode lookup table."""
    rows = [
        (1, "Bearing Failure", "Fatigue and wear", "Mechanical", "Maintenance"),
        (2, "Seal Leak", "Wear and contamination", "Mechanical", "Maintenance"),
        (3, "Overheating", "Thermal overload", "Process", "Operation"),
        (4, "Excessive Vibration", "Imbalance and misalignment", "Mechanical", "Installation"),
        (5, "Electrical Fault", "Insulation breakdown", "Electrical", "Manufacturing"),
        (6, "Corrosion", "External or internal corrosion", "Integrity", "Environment"),
        (7, "Erosion", "Flow-assisted wear", "Mechanical", "Operation"),
        (8, "Blockage", "Restriction or fouling", "Process", "Operation"),
        (9, "Control Failure", "Instrument or control malfunction", "Instrumentation", "Maintenance"),
        (10, "Other", "Unknown or uncategorised", "Other", "Unknown"),
    ]
    return pd.DataFrame(
        [
            {
                "FailureModeID": mode_id,
                "FailureMode": mode,
                "FailureMechanism": mechanism,
                "FailureClass": failure_class,
                "TypicalRootCause": root_cause,
                "DataOrigin": DATA_ORIGIN_FAILURE_MODE,
            }
            for mode_id, mode, mechanism, failure_class, root_cause in rows
        ],
        columns=DIM_FAILURE_MODE_COLUMNS,
    )


def build_dim_maintenance_action() -> pd.DataFrame:
    """Build stable maintenance-action lookup table."""
    rows = [
        (1, "Replace Bearing", "Corrective", "Mechanical"),
        (2, "Replace Seal", "Corrective", "Mechanical"),
        (3, "Realign Shaft", "Corrective", "Mechanical"),
        (4, "Lubricate Component", "Preventive", "Lubrication"),
        (5, "Inspect and Clean", "Preventive", "Inspection"),
        (6, "Replace Electrical Component", "Corrective", "Electrical"),
        (7, "Calibrate Instrument", "Preventive", "Instrumentation"),
        (8, "Overhaul Equipment", "Corrective", "Mechanical"),
        (9, "Repair Pipeline", "Corrective", "Pipeline"),
        (10, "Condition Monitoring Inspection", "Condition-Based", "Inspection"),
    ]
    return pd.DataFrame(
        [
            {
                "ActionID": action_id,
                "ActionDescription": description,
                "ActionType": action_type,
                "ActionCategory": category,
                "DataOrigin": DATA_ORIGIN_ACTION,
            }
            for action_id, description, action_type, category in rows
        ],
        columns=DIM_MAINTENANCE_ACTION_COLUMNS,
    )


FAILURE_CODE_TO_MODE_ID = {
    "comp1": 1,
    "comp2": 2,
    "comp3": 4,
    "comp4": 3,
}

FAILURE_DOWNTIME_HOURS = {
    1: 8.0,
    2: 8.0,
    3: 24.0,
    4: 16.0,
    5: 12.0,
    6: 18.0,
    7: 18.0,
    8: 10.0,
    9: 6.0,
    10: 8.0,
}

REPAIR_COST_BY_CATEGORY_MODE = {
    "Compressor": {1: 12000, 2: 9000, 3: 22000, 4: 18000},
    "Pump": {1: 8000, 2: 5000, 3: 14000, 4: 12000},
    "Electrical": {1: 6000, 2: 4000, 3: 10000, 4: 10000},
    "Generator": {1: 10000, 2: 6000, 3: 16000, 4: 15000},
    "Other": {1: 7000, 2: 5000, 3: 12000, 4: 10000},
}

HOURLY_LOSS_RATE = {
    "Compressor": 5000,
    "Pump": 3000,
    "Electrical": 2000,
    "Generator": 1500,
    "Other": 1000,
}


def failure_consequence(equipment_category: str, downtime_hours: float) -> str:
    """Classify consequence with a deterministic documented rule."""
    if equipment_category == "Compressor" or downtime_hours >= 20:
        return "High"
    if equipment_category in {"Pump", "Generator", "Electrical"} or downtime_hours >= 12:
        return "Medium"
    return "Low"


def build_fact_failure(
    sources: dict[str, pd.DataFrame],
    dim_failure_mode: pd.DataFrame,
) -> pd.DataFrame:
    """Build one fact row per Azure PdM failure event."""
    failures = sources["failures"].copy()
    asset_map = build_machine_asset_map(sources)
    mode_lookup = dim_failure_mode.set_index("FailureModeID")

    failures = failures.sort_values(["datetime", "machineID", "failure"]).reset_index(
        drop=True
    )
    failures = failures.merge(asset_map, on="machineID", how="left")
    failures["FailureModeID"] = failures["failure"].map(FAILURE_CODE_TO_MODE_ID)
    failures["DowntimeHours"] = failures["FailureModeID"].map(FAILURE_DOWNTIME_HOURS)
    failures["RepairHours"] = (failures["DowntimeHours"] * 0.8).round(2)
    failures["DowntimeEnd"] = failures["datetime"] + pd.to_timedelta(
        failures["DowntimeHours"], unit="h"
    )
    failures["FailureCause"] = failures["FailureModeID"].map(
        mode_lookup["TypicalRootCause"].to_dict()
    )
    failures["FailureConsequence"] = failures.apply(
        lambda row: failure_consequence(
            row["EquipmentCategory"], float(row["DowntimeHours"])
        ),
        axis=1,
    )
    failures["RepairCost"] = failures.apply(
        lambda row: REPAIR_COST_BY_CATEGORY_MODE.get(
            row["EquipmentCategory"], REPAIR_COST_BY_CATEGORY_MODE["Other"]
        ).get(int(row["FailureModeID"]), 7000),
        axis=1,
    )
    failures["ProductionLoss"] = failures.apply(
        lambda row: float(row["DowntimeHours"])
        * HOURLY_LOSS_RATE.get(row["EquipmentCategory"], HOURLY_LOSS_RATE["Other"]),
        axis=1,
    )

    repeat_sorted = failures.sort_values(
        ["AssetID", "FailureModeID", "datetime"]
    ).copy()
    previous_failure = repeat_sorted.groupby(["AssetID", "FailureModeID"])[
        "datetime"
    ].shift(1)
    repeat_sorted["IsRepeatFailure"] = (
        (repeat_sorted["datetime"] - previous_failure).dt.days <= 90
    ).fillna(False)
    failures = failures.merge(
        repeat_sorted[["AssetID", "FailureModeID", "datetime", "IsRepeatFailure"]],
        on=["AssetID", "FailureModeID", "datetime"],
        how="left",
    )

    fact = pd.DataFrame(
        {
            "EventID": range(1, len(failures) + 1),
            "AssetID": failures["AssetID"],
            "FailureDate": failures["datetime"].dt.date.astype(str),
            "FailureModeID": failures["FailureModeID"].astype(int),
            "DowntimeStart": failures["datetime"].dt.strftime("%Y-%m-%d %H:%M:%S"),
            "DowntimeEnd": failures["DowntimeEnd"].dt.strftime("%Y-%m-%d %H:%M:%S"),
            "DowntimeHours": failures["DowntimeHours"].astype(float),
            "RepairHours": failures["RepairHours"].astype(float),
            "FailureCause": failures["FailureCause"],
            "FailureConsequence": failures["FailureConsequence"],
            "RepairCost": failures["RepairCost"].astype(float),
            "ProductionLoss": failures["ProductionLoss"].astype(float),
            "IsRepeatFailure": failures["IsRepeatFailure"].astype(bool),
            "DataOrigin": DATA_ORIGIN_FAILURE,
            "IsIllustrative": True,
        },
        columns=FACT_FAILURE_COLUMNS,
    )
    return fact


ACTION_CODE_TO_ACTION_ID = {
    "comp1": 1,
    "comp2": 2,
    "comp3": 8,
    "comp4": 4,
}

BASE_ACTION_LABOR = {
    1: 4.0,
    2: 4.0,
    3: 5.0,
    4: 3.0,
    5: 2.0,
    6: 5.0,
    7: 2.0,
    8: 12.0,
    9: 8.0,
    10: 2.0,
}

BASE_ACTION_PARTS = {
    1: 5000,
    2: 3000,
    3: 2500,
    4: 800,
    5: 600,
    6: 4500,
    7: 900,
    8: 12000,
    9: 10000,
    10: 300,
}


@dataclass(frozen=True)
class EventWindow:
    machine_id: int
    timestamp: pd.Timestamp
    code: str | None = None


def build_event_windows(df: pd.DataFrame, code_column: str | None) -> dict[int, list[EventWindow]]:
    """Group source event timestamps by machine for proximity checks."""
    grouped: dict[int, list[EventWindow]] = {}
    for _, row in df.sort_values("datetime").iterrows():
        machine_id = int(row["machineID"])
        code = str(row[code_column]) if code_column else None
        grouped.setdefault(machine_id, []).append(
            EventWindow(machine_id, pd.Timestamp(row["datetime"]), code)
        )
    return grouped


def has_event_within(
    events_by_machine: dict[int, list[EventWindow]],
    machine_id: int,
    timestamp: pd.Timestamp,
    days: int,
    code: str | None = None,
) -> bool:
    """Return whether a machine has an event within a +/- day window."""
    for event in events_by_machine.get(machine_id, []):
        if code is not None and event.code != code:
            continue
        if abs((event.timestamp - timestamp).total_seconds()) <= days * 24 * 60 * 60:
            return True
    return False


def maintenance_type_for_row(
    row: pd.Series,
    failures_by_machine: dict[int, list[EventWindow]],
    errors_by_machine: dict[int, list[EventWindow]],
) -> str:
    """Classify maintenance type from failure/error proximity."""
    machine_id = int(row["machineID"])
    timestamp = pd.Timestamp(row["datetime"])
    code = str(row["comp"])

    if has_event_within(failures_by_machine, machine_id, timestamp, 2, code=code):
        return "Corrective"
    if has_event_within(errors_by_machine, machine_id, timestamp, 3):
        return "Condition-Based"
    if has_event_within(errors_by_machine, machine_id, timestamp, 14):
        return "Predictive"
    return "Preventive"


def performed_by(machine_id: int, equipment_category: str, maintenance_type: str) -> str:
    """Assign a deterministic maintenance team."""
    if maintenance_type == "Condition-Based":
        return "Reliability Team"
    if equipment_category in {"Compressor", "Pump"}:
        return "Mechanical Team A" if machine_id % 2 else "Mechanical Team B"
    if equipment_category in {"Electrical", "Generator"}:
        return "Electrical Team"
    return "Maintenance Team"


def parts_multiplier(equipment_category: str) -> float:
    if equipment_category == "Compressor":
        return 1.5
    if equipment_category == "Generator":
        return 1.25
    if equipment_category == "Pump":
        return 1.1
    return 1.0


def build_fact_maintenance(sources: dict[str, pd.DataFrame]) -> pd.DataFrame:
    """Build one fact row per Azure PdM maintenance event."""
    maint = sources["maintenance"].copy()
    asset_map = build_machine_asset_map(sources)
    failures_by_machine = build_event_windows(sources["failures"], "failure")
    errors_by_machine = build_event_windows(sources["errors"], "errorID")

    maint = maint.sort_values(["datetime", "machineID", "comp"]).reset_index(drop=True)
    maint = maint.merge(asset_map, on="machineID", how="left")
    maint["ActionID"] = maint["comp"].map(ACTION_CODE_TO_ACTION_ID).astype(int)
    maint["MaintenanceType"] = maint.apply(
        lambda row: maintenance_type_for_row(row, failures_by_machine, errors_by_machine),
        axis=1,
    )
    maint["LaborHours"] = maint.apply(
        lambda row: max(
            1.5,
            BASE_ACTION_LABOR[int(row["ActionID"])]
            * (0.75 if row["MaintenanceType"] in {"Predictive", "Condition-Based"} else 1.0),
        ),
        axis=1,
    ).round(2)
    maint["PartsCost"] = maint.apply(
        lambda row: round(
            BASE_ACTION_PARTS[int(row["ActionID"])]
            * parts_multiplier(row["EquipmentCategory"]),
            2,
        ),
        axis=1,
    )
    maint["TotalCost"] = (maint["LaborHours"] * 150 + maint["PartsCost"]).round(2)
    maint["CompletionDate"] = maint.apply(
        lambda row: (
            pd.Timestamp(row["datetime"]) + pd.Timedelta(days=1)
            if float(row["LaborHours"]) > 8
            else pd.Timestamp(row["datetime"])
        ).date(),
        axis=1,
    )
    maint["PerformedBy"] = maint.apply(
        lambda row: performed_by(
            int(row["machineID"]), row["EquipmentCategory"], row["MaintenanceType"]
        ),
        axis=1,
    )

    return pd.DataFrame(
        {
            "WorkOrderID": range(1, len(maint) + 1),
            "AssetID": maint["AssetID"],
            "MaintenanceDate": maint["datetime"].dt.date.astype(str),
            "ActionID": maint["ActionID"].astype(int),
            "MaintenanceType": maint["MaintenanceType"],
            "LaborHours": maint["LaborHours"].astype(float),
            "PartsCost": maint["PartsCost"].astype(float),
            "TotalCost": maint["TotalCost"].astype(float),
            "WorkOrderStatus": "Completed",
            "CompletionDate": maint["CompletionDate"].astype(str),
            "PerformedBy": maint["PerformedBy"],
            "DataOrigin": DATA_ORIGIN_MAINTENANCE,
            "IsIllustrative": True,
        },
        columns=FACT_MAINTENANCE_COLUMNS,
    )


PM_STRATEGY = {
    "Compressor": {
        "frequency": "Monthly",
        "months": 1,
        "categories": ["Inspection", "Lubrication", "Condition Monitoring"],
    },
    "Pump": {
        "frequency": "Monthly",
        "months": 1,
        "categories": ["Inspection", "Lubrication"],
    },
    "Electrical": {
        "frequency": "Quarterly",
        "months": 3,
        "categories": ["Inspection", "Electrical Test", "Calibration"],
    },
    "Generator": {
        "frequency": "Quarterly",
        "months": 3,
        "categories": ["Inspection", "Electrical Test", "Overhaul Review"],
    },
    "Other": {
        "frequency": "Quarterly",
        "months": 3,
        "categories": ["Inspection"],
    },
}


def assigned_pm_team(equipment_category: str, pm_category: str) -> str:
    if pm_category in {"Calibration", "Condition Monitoring"}:
        return "I&C"
    if equipment_category in {"Electrical", "Generator"}:
        return "Elec"
    return "Mech"


def pm_status(asset_id: str, due_date: date) -> tuple[str, str, str | None, int | None]:
    """Return deterministic PM completion and schedule status fields."""
    rng = stable_rng(f"{asset_id}|{due_date.isoformat()}")

    if due_date > PROJECT_CURRENT_DATE:
        if rng.random() < 0.04:
            return "Cancelled", "Upcoming", None, None
        return "Open", "Upcoming", None, None

    draw = rng.random()
    if draw < 0.70:
        days_early = rng.randint(0, 3)
        completed = pd.Timestamp(due_date) - pd.Timedelta(days=days_early)
        return "Completed", "On Time", completed.date().isoformat(), None
    if draw < 0.85:
        days_late = rng.randint(1, 14)
        completed = pd.Timestamp(due_date) + pd.Timedelta(days=days_late)
        return "Completed", "Completed Late", completed.date().isoformat(), None
    if draw < 0.95:
        days_overdue = (PROJECT_CURRENT_DATE - due_date).days
        return "Open", "Overdue", None, int(days_overdue)
    return "Cancelled", "Upcoming", None, None


def build_fact_pm_compliance(dim_asset: pd.DataFrame) -> pd.DataFrame:
    """Build an illustrative PM compliance table linked to dim_asset."""
    rows: list[dict] = []
    record_id = 1
    schedule_start = date(2024, 1, 1)
    schedule_end = date(2026, 12, 31)

    for _, asset in dim_asset.sort_values("AssetID").iterrows():
        equipment_category = str(asset["EquipmentCategory"])
        strategy = PM_STRATEGY.get(equipment_category, PM_STRATEGY["Other"])
        due_date = schedule_start
        sequence = 0

        while due_date <= schedule_end:
            pm_category = strategy["categories"][sequence % len(strategy["categories"])]
            completion_status, schedule_status, completed_date, days_overdue = pm_status(
                str(asset["AssetID"]), due_date
            )
            rows.append(
                {
                    "PMRecordID": record_id,
                    "AssetID": asset["AssetID"],
                    "PMDueDate": due_date.isoformat(),
                    "PMCompletedDate": completed_date,
                    "PMCategory": pm_category,
                    "PMFrequency": strategy["frequency"],
                    "AssignedTeam": assigned_pm_team(equipment_category, pm_category),
                    "CompletionStatus": completion_status,
                    "ScheduleStatus": schedule_status,
                    "DaysOverdue": days_overdue,
                    "DataOrigin": DATA_ORIGIN_PM,
                    "IsIllustrative": True,
                }
            )
            record_id += 1
            sequence += 1
            due_date = add_months(due_date, int(strategy["months"]))

    return pd.DataFrame(rows, columns=FACT_PM_COLUMNS)


def output_path(output_dir: Path, logical_name: str) -> Path:
    return output_dir / OUTPUT_FILES[logical_name]


def write_outputs(tables: dict[str, pd.DataFrame], output_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    for name, df in tables.items():
        df.to_csv(output_path(output_dir, name), index=False)


def build_powerbi_v02_data(
    output_dir: Path | None = None,
    quiet: bool = False,
) -> dict[str, pd.DataFrame]:
    """Build all six Power BI v0.2 tables and write CSV outputs."""
    output_dir = output_dir or PROCESSED_DIR
    sources = read_sources()

    dim_asset = build_dim_asset(sources)
    dim_failure_mode = build_dim_failure_mode()
    dim_maintenance_action = build_dim_maintenance_action()
    fact_failure = build_fact_failure(sources, dim_failure_mode)
    fact_maintenance = build_fact_maintenance(sources)
    fact_pm_compliance = build_fact_pm_compliance(dim_asset)

    tables = {
        "dim_asset": dim_asset,
        "fact_failure": fact_failure,
        "fact_maintenance": fact_maintenance,
        "fact_pm_compliance": fact_pm_compliance,
        "dim_failure_mode": dim_failure_mode,
        "dim_maintenance_action": dim_maintenance_action,
    }

    write_outputs(tables, output_dir)

    if not quiet:
        print("Power BI v0.2 data build complete.")
        print(f"Output folder: {output_dir.relative_to(PROJECT_ROOT)}")
        print()
        for name, df in tables.items():
            print(f"{OUTPUT_FILES[name]}: {len(df):,} rows, {len(df.columns)} columns")
            print("  " + ", ".join(df.columns))

    return tables


def generate_temp_outputs() -> dict[str, bytes]:
    """Build outputs in a temporary folder and return file bytes for validation."""
    with TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)
        build_powerbi_v02_data(output_dir=temp_path, quiet=True)
        return {
            file_name: (temp_path / file_name).read_bytes()
            for file_name in OUTPUT_FILES.values()
        }


def main() -> None:
    build_powerbi_v02_data()


if __name__ == "__main__":
    main()
