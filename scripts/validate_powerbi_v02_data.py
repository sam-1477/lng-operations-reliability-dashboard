"""Validate Power BI v0.2 star-schema CSV outputs.

Run from the project root:
    python scripts\\validate_powerbi_v02_data.py
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Callable

import sys

try:
    import pandas as pd
except ImportError as error:  # pragma: no cover - runtime dependency guard
    raise SystemExit(
        "This script requires pandas. Install project dependencies first."
    ) from error

import build_powerbi_v02_data as build


PROJECT_ROOT = Path(__file__).resolve().parents[1]
PROCESSED_DIR = PROJECT_ROOT / "data" / "processed"
REPORT_PATH = PROJECT_ROOT / "docs" / "powerbi_v0.2_data_validation_report.md"

EXPECTED_COLUMNS = {
    "dim_asset": build.DIM_ASSET_COLUMNS,
    "fact_failure": build.FACT_FAILURE_COLUMNS,
    "fact_maintenance": build.FACT_MAINTENANCE_COLUMNS,
    "fact_pm_compliance": build.FACT_PM_COLUMNS,
    "dim_failure_mode": build.DIM_FAILURE_MODE_COLUMNS,
    "dim_maintenance_action": build.DIM_MAINTENANCE_ACTION_COLUMNS,
}

PRIMARY_KEYS = {
    "dim_asset": "AssetID",
    "fact_failure": "EventID",
    "fact_maintenance": "WorkOrderID",
    "fact_pm_compliance": "PMRecordID",
    "dim_failure_mode": "FailureModeID",
    "dim_maintenance_action": "ActionID",
}

NUMERIC_COLUMNS = {
    "fact_failure": [
        "EventID",
        "FailureModeID",
        "DowntimeHours",
        "RepairHours",
        "RepairCost",
        "ProductionLoss",
    ],
    "fact_maintenance": ["WorkOrderID", "ActionID", "LaborHours", "PartsCost", "TotalCost"],
    "fact_pm_compliance": ["PMRecordID", "DaysOverdue"],
    "dim_failure_mode": ["FailureModeID"],
    "dim_maintenance_action": ["ActionID"],
}

DATE_COLUMNS = {
    "dim_asset": {"InstallDate": False},
    "fact_failure": {
        "FailureDate": False,
        "DowntimeStart": False,
        "DowntimeEnd": False,
    },
    "fact_maintenance": {
        "MaintenanceDate": False,
        "CompletionDate": False,
    },
    "fact_pm_compliance": {
        "PMDueDate": False,
        "PMCompletedDate": True,
    },
}

TABLES_WITH_IS_ILLUSTRATIVE = [
    "dim_asset",
    "fact_failure",
    "fact_maintenance",
    "fact_pm_compliance",
]


@dataclass
class CheckResult:
    name: str
    passed: bool
    detail: str


class Validator:
    """Collect validation checks and report results."""

    def __init__(self) -> None:
        self.results: list[CheckResult] = []

    def check(self, name: str, fn: Callable[[], str]) -> None:
        try:
            detail = fn()
            self.results.append(CheckResult(name, True, detail))
            print(f"PASS - {name}: {detail}")
        except AssertionError as error:
            detail = str(error) or "Assertion failed"
            self.results.append(CheckResult(name, False, detail))
            print(f"FAIL - {name}: {detail}")
        except Exception as error:  # pragma: no cover - defensive reporting
            detail = f"{type(error).__name__}: {error}"
            self.results.append(CheckResult(name, False, detail))
            print(f"FAIL - {name}: {detail}")

    @property
    def passed(self) -> bool:
        return all(result.passed for result in self.results)


def csv_path(table_name: str) -> Path:
    return PROCESSED_DIR / build.OUTPUT_FILES[table_name]


def is_blank_series(series: pd.Series) -> pd.Series:
    return series.isna() | (series.astype(str).str.strip() == "")


def parse_bool_series(series: pd.Series) -> pd.Series:
    mapping = {
        True: True,
        False: False,
        "True": True,
        "False": False,
        "TRUE": True,
        "FALSE": False,
        "true": True,
        "false": False,
        "1": True,
        "0": False,
    }
    return series.map(mapping)


def load_tables() -> dict[str, pd.DataFrame]:
    tables: dict[str, pd.DataFrame] = {}
    for table_name in EXPECTED_COLUMNS:
        path = csv_path(table_name)
        if path.exists():
            tables[table_name] = pd.read_csv(path)
    return tables


def check_required_files_exist() -> str:
    missing = [str(csv_path(name).relative_to(PROJECT_ROOT)) for name in EXPECTED_COLUMNS if not csv_path(name).exists()]
    assert not missing, "Missing files: " + ", ".join(missing)
    return "all six required CSV files exist"


def check_exact_columns(tables: dict[str, pd.DataFrame]) -> str:
    mismatches = []
    for table_name, expected in EXPECTED_COLUMNS.items():
        actual = list(tables[table_name].columns)
        if actual != expected:
            mismatches.append(
                f"{table_name}: expected {expected}, got {actual}"
            )
    assert not mismatches, "; ".join(mismatches)
    return "all table schemas match the required column order"


def check_primary_keys_unique(tables: dict[str, pd.DataFrame]) -> str:
    problems = []
    for table_name, pk in PRIMARY_KEYS.items():
        duplicates = int(tables[table_name][pk].duplicated().sum())
        if duplicates:
            problems.append(f"{table_name}.{pk} duplicates={duplicates}")
    assert not problems, "; ".join(problems)
    return "all primary keys are unique"


def check_no_blank_primary_keys(tables: dict[str, pd.DataFrame]) -> str:
    problems = []
    for table_name, pk in PRIMARY_KEYS.items():
        blanks = int(is_blank_series(tables[table_name][pk]).sum())
        if blanks:
            problems.append(f"{table_name}.{pk} blanks={blanks}")
    assert not problems, "; ".join(problems)
    return "no blank primary keys"


def check_no_blank_fact_asset_ids(tables: dict[str, pd.DataFrame]) -> str:
    problems = []
    for table_name in ["fact_failure", "fact_maintenance", "fact_pm_compliance"]:
        blanks = int(is_blank_series(tables[table_name]["AssetID"]).sum())
        if blanks:
            problems.append(f"{table_name}.AssetID blanks={blanks}")
    assert not problems, "; ".join(problems)
    return "fact AssetID columns are populated"


def check_asset_relationships(tables: dict[str, pd.DataFrame]) -> str:
    asset_ids = set(tables["dim_asset"]["AssetID"].astype(str))
    problems = []
    for table_name in ["fact_failure", "fact_maintenance", "fact_pm_compliance"]:
        fact_assets = set(tables[table_name]["AssetID"].astype(str))
        missing = sorted(fact_assets - asset_ids)
        if missing:
            problems.append(f"{table_name} missing AssetIDs={missing[:5]}")
    assert not problems, "; ".join(problems)
    return "all fact AssetIDs exist in dim_asset"


def check_failure_mode_relationship(tables: dict[str, pd.DataFrame]) -> str:
    valid = set(pd.to_numeric(tables["dim_failure_mode"]["FailureModeID"]))
    observed = set(pd.to_numeric(tables["fact_failure"]["FailureModeID"]))
    missing = sorted(observed - valid)
    assert not missing, f"missing FailureModeID values: {missing}"
    return "all fact_failure FailureModeID values exist in dim_failure_mode"


def check_action_relationship(tables: dict[str, pd.DataFrame]) -> str:
    valid = set(pd.to_numeric(tables["dim_maintenance_action"]["ActionID"]))
    observed = set(pd.to_numeric(tables["fact_maintenance"]["ActionID"]))
    missing = sorted(observed - valid)
    assert not missing, f"missing ActionID values: {missing}"
    return "all fact_maintenance ActionID values exist in dim_maintenance_action"


def require_numeric(series: pd.Series, allow_blank: bool = False) -> pd.Series:
    blank = is_blank_series(series)
    values = pd.to_numeric(series, errors="coerce")
    invalid = values.isna() & ~blank
    if not allow_blank:
        invalid = invalid | blank
    assert not invalid.any(), f"invalid numeric values in {series.name}: {int(invalid.sum())}"
    return values


def check_no_negative_downtime(tables: dict[str, pd.DataFrame]) -> str:
    downtime = require_numeric(tables["fact_failure"]["DowntimeHours"])
    assert not (downtime < 0).any(), "negative DowntimeHours found"
    return "no negative downtime"


def check_no_negative_repair_hours(tables: dict[str, pd.DataFrame]) -> str:
    repair = require_numeric(tables["fact_failure"]["RepairHours"])
    assert not (repair < 0).any(), "negative RepairHours found"
    return "no negative repair hours"


def check_repair_hours_not_greater_than_downtime(tables: dict[str, pd.DataFrame]) -> str:
    repair = require_numeric(tables["fact_failure"]["RepairHours"])
    downtime = require_numeric(tables["fact_failure"]["DowntimeHours"])
    assert not (repair > downtime).any(), "RepairHours greater than DowntimeHours"
    return "RepairHours <= DowntimeHours"


def check_downtime_end_after_start(tables: dict[str, pd.DataFrame]) -> str:
    start = pd.to_datetime(tables["fact_failure"]["DowntimeStart"], errors="coerce")
    end = pd.to_datetime(tables["fact_failure"]["DowntimeEnd"], errors="coerce")
    assert not start.isna().any(), "invalid DowntimeStart values"
    assert not end.isna().any(), "invalid DowntimeEnd values"
    assert not (end < start).any(), "DowntimeEnd before DowntimeStart"
    return "DowntimeEnd >= DowntimeStart"


def check_no_negative_labor_or_costs(tables: dict[str, pd.DataFrame]) -> str:
    problems = []
    checks = {
        "fact_failure.RepairCost": tables["fact_failure"]["RepairCost"],
        "fact_failure.ProductionLoss": tables["fact_failure"]["ProductionLoss"],
        "fact_maintenance.LaborHours": tables["fact_maintenance"]["LaborHours"],
        "fact_maintenance.PartsCost": tables["fact_maintenance"]["PartsCost"],
        "fact_maintenance.TotalCost": tables["fact_maintenance"]["TotalCost"],
    }
    for label, series in checks.items():
        values = require_numeric(series)
        negatives = int((values < 0).sum())
        if negatives:
            problems.append(f"{label} negatives={negatives}")
    assert not problems, "; ".join(problems)
    return "no negative labor hours or costs"


def check_completion_date_after_maintenance_date(tables: dict[str, pd.DataFrame]) -> str:
    maintenance = pd.to_datetime(tables["fact_maintenance"]["MaintenanceDate"], errors="coerce")
    completion = pd.to_datetime(tables["fact_maintenance"]["CompletionDate"], errors="coerce")
    assert not maintenance.isna().any(), "invalid MaintenanceDate values"
    assert not completion.isna().any(), "invalid CompletionDate values"
    assert not (completion < maintenance).any(), "CompletionDate before MaintenanceDate"
    return "CompletionDate >= MaintenanceDate"


def check_pm_status_consistency(tables: dict[str, pd.DataFrame]) -> str:
    pm = tables["fact_pm_compliance"].copy()
    due = pd.to_datetime(pm["PMDueDate"], errors="coerce")
    completed = pd.to_datetime(pm["PMCompletedDate"], errors="coerce")
    completion_status = pm["CompletionStatus"].astype(str)
    schedule_status = pm["ScheduleStatus"].astype(str)

    allowed_completion = {"Completed", "Open", "Cancelled"}
    allowed_schedule = {"On Time", "Completed Late", "Overdue", "Upcoming"}
    assert set(completion_status).issubset(allowed_completion), "invalid CompletionStatus"
    assert set(schedule_status).issubset(allowed_schedule), "invalid ScheduleStatus"
    assert not due.isna().any(), "invalid PMDueDate values"

    completed_mask = completion_status == "Completed"
    open_mask = completion_status == "Open"
    cancelled_mask = completion_status == "Cancelled"

    assert not completed[completed_mask].isna().any(), "Completed PM with blank PMCompletedDate"
    assert completed[open_mask].isna().all(), "Open PM with PMCompletedDate"
    assert completed[cancelled_mask].isna().all(), "Cancelled PM with PMCompletedDate"

    on_time = schedule_status == "On Time"
    late = schedule_status == "Completed Late"
    overdue = schedule_status == "Overdue"
    upcoming = schedule_status == "Upcoming"
    project_now = pd.Timestamp(build.PROJECT_CURRENT_DATE)

    assert (completion_status[on_time] == "Completed").all(), "On Time PM not completed"
    assert (completed[on_time] <= due[on_time]).all(), "On Time PM completed after due date"
    assert (completion_status[late] == "Completed").all(), "Completed Late PM not completed"
    assert (completed[late] > due[late]).all(), "Completed Late PM not after due date"
    assert (completion_status[overdue] == "Open").all(), "Overdue PM not open"
    assert completed[overdue].isna().all(), "Overdue PM has PMCompletedDate"
    assert (due[overdue] < project_now).all(), "Overdue PM not before project current date"
    assert ((due[upcoming] > project_now) | cancelled_mask[upcoming]).all(), (
        "Upcoming PM is neither future-due nor cancelled"
    )

    return "PM completion and schedule statuses are internally consistent"


def check_days_overdue_consistency(tables: dict[str, pd.DataFrame]) -> str:
    pm = tables["fact_pm_compliance"].copy()
    due = pd.to_datetime(pm["PMDueDate"], errors="coerce")
    days = require_numeric(pm["DaysOverdue"], allow_blank=True)
    overdue = pm["ScheduleStatus"].astype(str) == "Overdue"
    expected = (pd.Timestamp(build.PROJECT_CURRENT_DATE) - due).dt.days

    assert not days[overdue].isna().any(), "Overdue records with blank DaysOverdue"
    assert (days[overdue] > 0).all(), "Overdue records must have positive DaysOverdue"
    assert (days[overdue].astype(int) == expected[overdue].astype(int)).all(), (
        "DaysOverdue does not equal project current date minus PMDueDate"
    )
    non_overdue = ~overdue
    assert (days[non_overdue].isna() | (days[non_overdue] == 0)).all(), (
        "Non-overdue records must have blank or zero DaysOverdue"
    )
    return "DaysOverdue is positive only for Overdue PM records"


def check_valid_date_parsing(tables: dict[str, pd.DataFrame]) -> str:
    problems = []
    for table_name, columns in DATE_COLUMNS.items():
        for column, allow_blank in columns.items():
            series = tables[table_name][column]
            parsed = pd.to_datetime(series, errors="coerce")
            invalid = parsed.isna()
            if allow_blank:
                invalid = invalid & ~is_blank_series(series)
            if invalid.any():
                problems.append(f"{table_name}.{column} invalid={int(invalid.sum())}")
    assert not problems, "; ".join(problems)
    return "all required date columns parse successfully"


def check_no_mixed_numeric_types(tables: dict[str, pd.DataFrame]) -> str:
    for table_name, columns in NUMERIC_COLUMNS.items():
        for column in columns:
            allow_blank = table_name == "fact_pm_compliance" and column == "DaysOverdue"
            require_numeric(tables[table_name][column], allow_blank=allow_blank)
    return "required numeric columns parse without mixed text values"


def check_data_origin_populated(tables: dict[str, pd.DataFrame]) -> str:
    problems = []
    for table_name, df in tables.items():
        blanks = int(is_blank_series(df["DataOrigin"]).sum())
        if blanks:
            problems.append(f"{table_name}.DataOrigin blanks={blanks}")
    assert not problems, "; ".join(problems)
    return "DataOrigin populated in all six tables"


def check_is_illustrative_populated(tables: dict[str, pd.DataFrame]) -> str:
    problems = []
    for table_name in TABLES_WITH_IS_ILLUSTRATIVE:
        parsed = parse_bool_series(tables[table_name]["IsIllustrative"])
        blanks = int(parsed.isna().sum())
        if blanks:
            problems.append(f"{table_name}.IsIllustrative invalid/blanks={blanks}")
    assert not problems, "; ".join(problems)
    return "IsIllustrative populated and boolean where required"


def check_repeat_failure_logic(tables: dict[str, pd.DataFrame]) -> str:
    failures = tables["fact_failure"].copy()
    failures["DowntimeStartParsed"] = pd.to_datetime(failures["DowntimeStart"], errors="coerce")
    failures = failures.sort_values(["AssetID", "FailureModeID", "DowntimeStartParsed"])
    previous = failures.groupby(["AssetID", "FailureModeID"])["DowntimeStartParsed"].shift(1)
    expected = ((failures["DowntimeStartParsed"] - previous).dt.days <= 90).fillna(False)
    observed = parse_bool_series(failures["IsRepeatFailure"]).fillna(False)
    mismatches = int((expected.reset_index(drop=True) != observed.reset_index(drop=True)).sum())
    assert mismatches == 0, f"repeat-failure mismatch count={mismatches}"
    return "repeat-failure logic is reproducible"


def check_regeneration_identical() -> str:
    regenerated = build.generate_temp_outputs()
    mismatches = []
    for file_name in build.OUTPUT_FILES.values():
        current_path = PROCESSED_DIR / file_name
        current_bytes = current_path.read_bytes()
        if current_bytes != regenerated[file_name]:
            mismatches.append(file_name)
    assert not mismatches, "regenerated outputs differ: " + ", ".join(mismatches)
    return "same seed regenerates byte-identical outputs"


def build_report(tables: dict[str, pd.DataFrame], results: list[CheckResult]) -> str:
    lines = [
        "# Power BI v0.2 Data Validation Report",
        "",
        f"Validation date: {build.PROJECT_CURRENT_DATE.isoformat()}",
        "",
        "## Row Counts",
        "",
        "| Table | Rows | Columns |",
        "|---|---:|---:|",
    ]
    for table_name, df in tables.items():
        lines.append(f"| {build.OUTPUT_FILES[table_name]} | {len(df)} | {len(df.columns)} |")

    lines.extend(["", "## Table Schemas", ""])
    for table_name, df in tables.items():
        lines.extend(
            [
                f"### {build.OUTPUT_FILES[table_name]}",
                "",
                "```text",
                "\n".join(df.columns),
                "```",
                "",
            ]
        )

    lines.extend(
        [
            "## Validation Checks",
            "",
            "| Check | Result | Detail |",
            "|---|---|---|",
        ]
    )
    for result in results:
        status = "PASS" if result.passed else "FAIL"
        detail = result.detail.replace("|", "\\|")
        lines.append(f"| {result.name} | {status} | {detail} |")

    lines.extend(["", "## Field Provenance", ""])
    for table_name, fields in build.FIELD_PROVENANCE.items():
        lines.extend(
            [
                f"### {build.OUTPUT_FILES.get(table_name, table_name)}",
                "",
                "| Field | Provenance |",
                "|---|---|",
            ]
        )
        for field_name, provenance in fields.items():
            lines.append(f"| {field_name} | {provenance} |")
        lines.append("")

    verdict = "PASS" if all(result.passed for result in results) else "FAIL"
    lines.extend(["## Verdict", "", f"**Validation result:** {verdict}", ""])
    return "\n".join(lines)


def print_table_summaries(tables: dict[str, pd.DataFrame]) -> None:
    print("Power BI v0.2 data validation")
    print()
    print("Row counts and schemas:")
    for table_name, df in tables.items():
        print(f"- {build.OUTPUT_FILES[table_name]}: {len(df):,} rows")
        print("  " + ", ".join(df.columns))
    print()


def main() -> int:
    validator = Validator()

    validator.check("1. All required files exist", check_required_files_exist)
    if not validator.results[-1].passed:
        REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
        REPORT_PATH.write_text(build_report({}, validator.results), encoding="utf-8")
        return 1

    tables = load_tables()
    print_table_summaries(tables)

    validator.check("2. Exact required columns exist", lambda: check_exact_columns(tables))
    validator.check("3. Primary keys are unique", lambda: check_primary_keys_unique(tables))
    validator.check("4. No blank primary keys", lambda: check_no_blank_primary_keys(tables))
    validator.check("5. No blank AssetID values in fact tables", lambda: check_no_blank_fact_asset_ids(tables))
    validator.check("6. Every fact AssetID exists in dim_asset", lambda: check_asset_relationships(tables))
    validator.check("7. Every FailureModeID exists in dim_failure_mode", lambda: check_failure_mode_relationship(tables))
    validator.check("8. Every ActionID exists in dim_maintenance_action", lambda: check_action_relationship(tables))
    validator.check("9. No negative downtime", lambda: check_no_negative_downtime(tables))
    validator.check("10. No negative repair hours", lambda: check_no_negative_repair_hours(tables))
    validator.check("11. RepairHours <= DowntimeHours", lambda: check_repair_hours_not_greater_than_downtime(tables))
    validator.check("12. DowntimeEnd >= DowntimeStart", lambda: check_downtime_end_after_start(tables))
    validator.check("13. No negative labor hours or costs", lambda: check_no_negative_labor_or_costs(tables))
    validator.check("14. CompletionDate >= MaintenanceDate", lambda: check_completion_date_after_maintenance_date(tables))
    validator.check("15. PM status consistency", lambda: check_pm_status_consistency(tables))
    validator.check("16. DaysOverdue consistency", lambda: check_days_overdue_consistency(tables))
    validator.check("17. Valid date parsing", lambda: check_valid_date_parsing(tables))
    validator.check("18. No mixed data types in required numeric columns", lambda: check_no_mixed_numeric_types(tables))
    validator.check("19. DataOrigin populated", lambda: check_data_origin_populated(tables))
    validator.check("20. IsIllustrative populated where required", lambda: check_is_illustrative_populated(tables))
    validator.check("21. Repeat-failure logic is reproducible", lambda: check_repeat_failure_logic(tables))
    validator.check("22. Regeneration with same seed produces identical outputs", check_regeneration_identical)

    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    REPORT_PATH.write_text(build_report(tables, validator.results), encoding="utf-8")
    print()
    print(f"Validation report written: {REPORT_PATH.relative_to(PROJECT_ROOT)}")

    return 0 if validator.passed else 1


if __name__ == "__main__":
    sys.exit(main())
