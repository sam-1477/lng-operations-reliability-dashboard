"""
Build a dashboard-ready reliability summary from the public Azure PdM dataset.

This script reads raw Azure Predictive Maintenance CSV files from data/raw/.
It does not edit, delete, or overwrite any raw data. The outputs are:

- data/processed/azure_machine_reliability_summary.csv
- samples/azure/azure_machine_reliability_summary_sample.csv
- reports/azure_reliability_summary_report.md

Run from the project root:
    python scripts\\build_azure_reliability_summary.py
"""

from __future__ import annotations

from pathlib import Path

try:
    import pandas as pd
except ImportError as error:
    raise SystemExit(
        "This script requires pandas. Install project dependencies with: "
        "pip install -r requirements.txt"
    ) from error


# Project folders.
PROJECT_ROOT = Path(__file__).resolve().parents[1]
AZURE_RAW_DIR = PROJECT_ROOT / "data" / "raw" / "extracted" / "azure_pdm"
PROCESSED_OUTPUT_PATH = (
    PROJECT_ROOT / "data" / "processed" / "azure_machine_reliability_summary.csv"
)
SAMPLE_OUTPUT_PATH = (
    PROJECT_ROOT / "samples" / "azure" / "azure_machine_reliability_summary_sample.csv"
)
REPORT_OUTPUT_PATH = PROJECT_ROOT / "reports" / "azure_reliability_summary_report.md"

# Raw Azure source files.
MACHINES_FILE = AZURE_RAW_DIR / "PdM_machines.csv"
TELEMETRY_FILE = AZURE_RAW_DIR / "PdM_telemetry.csv"
ERRORS_FILE = AZURE_RAW_DIR / "PdM_errors.csv"
FAILURES_FILE = AZURE_RAW_DIR / "PdM_failures.csv"
MAINT_FILE = AZURE_RAW_DIR / "PdM_maint.csv"

REQUIRED_FILES = [
    MACHINES_FILE,
    TELEMETRY_FILE,
    ERRORS_FILE,
    FAILURES_FILE,
    MAINT_FILE,
]

SAMPLE_ROW_LIMIT = 100
ASSUMED_DOWNTIME_HOURS_PER_FAILURE = 8


def check_required_files() -> None:
    """Stop with a clear message if any expected raw files are missing."""
    missing_files = [path for path in REQUIRED_FILES if not path.exists()]

    if not missing_files:
        return

    print("Missing required Azure PdM source files:")
    for path in missing_files:
        print(f"- {path}")

    raise SystemExit(
        "Place the extracted Azure PdM CSV files in "
        "data/raw/extracted/azure_pdm/ and rerun this script."
    )


def get_lng_asset_mapping(machine_id: int) -> dict[str, str]:
    """
    Map each public Azure machine into an LNG-style equipment category.

    This is a portfolio mapping for dashboard demonstration only. It does not
    identify real LNG plant assets.
    """
    category_cycle = {
        1: {
            "prefix": "PMP",
            "category": "Process Pumps",
            "name": "Process Pump",
        },
        2: {
            "prefix": "CMP",
            "category": "Gas Compressors",
            "name": "Gas Compressor",
        },
        3: {
            "prefix": "MTR",
            "category": "Electric Motors",
            "name": "Electric Motor",
        },
        4: {
            "prefix": "GEN",
            "category": "Utility Generators",
            "name": "Utility Generator",
        },
        0: {
            "prefix": "CWP",
            "category": "Cooling Water Pumps",
            "name": "Cooling Water Pump",
        },
    }

    category = category_cycle[machine_id % 5]
    asset_number = f"{machine_id:03d}"

    return {
        "lng_asset_id": f"LNG-{category['prefix']}-{asset_number}",
        "lng_asset_name": f"{category['name']} {asset_number}",
        "lng_equipment_category": category["category"],
    }


def clip_percent(value: float) -> float:
    """Keep a calculated percentage between 0 and 100."""
    return max(0.0, min(100.0, value))


def calculate_vibration_penalty(
    machine_avg_vibration: float, dataset_avg_vibration: float
) -> float:
    """
    Penalize machines with average vibration above the dataset average.

    The penalty is intentionally simple: every 10% above the dataset average
    subtracts about 2 points, capped at 15 points.
    """
    if dataset_avg_vibration <= 0 or machine_avg_vibration <= dataset_avg_vibration:
        return 0.0

    vibration_ratio = machine_avg_vibration / dataset_avg_vibration
    penalty = (vibration_ratio - 1.0) * 20.0
    return min(15.0, penalty)


def calculate_health_score(row: pd.Series, dataset_avg_vibration: float) -> float:
    """Calculate a simple 0-100 asset health score."""
    vibration_penalty = calculate_vibration_penalty(
        row["avg_vibration"], dataset_avg_vibration
    )

    score = (
        100.0
        - (row["failure_count"] * 12.0)
        - (row["error_count"] * 0.2)
        - (row["maintenance_event_count"] * 0.5)
        - vibration_penalty
    )

    return round(clip_percent(score), 1)


def assign_maintenance_priority(row: pd.Series) -> str:
    """Assign a plain-language maintenance priority for dashboard filtering."""
    if row["asset_health_score"] < 60 or row["failure_count"] >= 3:
        return "Critical"
    if row["asset_health_score"] < 75 or row["failure_count"] >= 2:
        return "High"
    if row["asset_health_score"] < 90 or row["error_count"] > 20:
        return "Medium"
    return "Low"


def build_engineering_note(priority: str) -> str:
    """Create a short note that can be shown in the dashboard."""
    notes = {
        "Critical": "Review immediately. Repeated failures or poor health score detected.",
        "High": "Plan inspection during next maintenance window.",
        "Medium": "Monitor trend and review maintenance history.",
        "Low": "Normal monitoring recommended.",
    }
    return notes[priority]


def build_summary_table() -> pd.DataFrame:
    """Read Azure data and build one reliability summary row per machine."""
    print("Reading raw Azure PdM files from data/raw/extracted/azure_pdm/")
    machines = pd.read_csv(MACHINES_FILE)
    telemetry = pd.read_csv(TELEMETRY_FILE)
    errors = pd.read_csv(ERRORS_FILE)
    failures = pd.read_csv(FAILURES_FILE)
    maint = pd.read_csv(MAINT_FILE)

    print("Calculating telemetry counts and average sensor values...")
    telemetry_summary = (
        telemetry.groupby("machineID")
        .agg(
            telemetry_record_count=("machineID", "size"),
            avg_voltage=("volt", "mean"),
            avg_rotate=("rotate", "mean"),
            avg_pressure=("pressure", "mean"),
            avg_vibration=("vibration", "mean"),
        )
        .reset_index()
    )

    print("Counting errors, failures, and maintenance events...")
    error_summary = (
        errors.groupby("machineID").size().reset_index(name="error_count")
    )
    maint_summary = (
        maint.groupby("machineID")
        .size()
        .reset_index(name="maintenance_event_count")
    )
    failure_summary = (
        failures.groupby("machineID").size().reset_index(name="failure_count")
    )

    print("Finding most recent failure type for each machine...")
    failures_with_datetime = failures.copy()
    failures_with_datetime["datetime"] = pd.to_datetime(
        failures_with_datetime["datetime"]
    )
    last_failure = (
        failures_with_datetime.sort_values("datetime")
        .groupby("machineID")
        .tail(1)[["machineID", "failure"]]
        .rename(columns={"failure": "last_failure_type"})
    )

    print("Combining machine information into one dashboard-ready table...")
    summary = machines.merge(telemetry_summary, on="machineID", how="left")
    summary = summary.merge(error_summary, on="machineID", how="left")
    summary = summary.merge(maint_summary, on="machineID", how="left")
    summary = summary.merge(failure_summary, on="machineID", how="left")
    summary = summary.merge(last_failure, on="machineID", how="left")

    # Machines with no events should show zero counts instead of blanks.
    count_columns = [
        "telemetry_record_count",
        "error_count",
        "maintenance_event_count",
        "failure_count",
    ]
    summary[count_columns] = summary[count_columns].fillna(0).astype(int)
    summary["last_failure_type"] = summary["last_failure_type"].fillna("None")

    # Add LNG-style portfolio asset fields.
    asset_mapping = summary["machineID"].apply(get_lng_asset_mapping).apply(pd.Series)
    summary = pd.concat([summary, asset_mapping], axis=1)

    print("Calculating MTBF-style, MTTR-style, availability-style, and health KPIs...")
    summary["estimated_downtime_hours"] = (
        summary["failure_count"] * ASSUMED_DOWNTIME_HOURS_PER_FAILURE
    )

    summary["mtbf_style_hours"] = summary.apply(
        lambda row: row["telemetry_record_count"] / row["failure_count"]
        if row["failure_count"] > 0
        else row["telemetry_record_count"],
        axis=1,
    )

    summary["mttr_style_hours"] = summary.apply(
        lambda row: row["estimated_downtime_hours"] / row["failure_count"]
        if row["failure_count"] > 0
        else 0,
        axis=1,
    )

    summary["availability_style_percent"] = summary.apply(
        lambda row: clip_percent(
            (
                (row["telemetry_record_count"] - row["estimated_downtime_hours"])
                / row["telemetry_record_count"]
            )
            * 100
        )
        if row["telemetry_record_count"] > 0
        else 0,
        axis=1,
    )

    dataset_avg_vibration = telemetry["vibration"].mean()
    summary["asset_health_score"] = summary.apply(
        calculate_health_score, axis=1, dataset_avg_vibration=dataset_avg_vibration
    )
    summary["maintenance_priority"] = summary.apply(
        assign_maintenance_priority, axis=1
    )
    summary["engineering_note"] = summary["maintenance_priority"].apply(
        build_engineering_note
    )

    # Round dashboard values so the CSV is easy to read.
    rounded_columns = [
        "avg_voltage",
        "avg_rotate",
        "avg_pressure",
        "avg_vibration",
        "mtbf_style_hours",
        "mttr_style_hours",
        "availability_style_percent",
    ]
    summary[rounded_columns] = summary[rounded_columns].round(2)

    output_columns = [
        "machineID",
        "model",
        "age",
        "lng_asset_id",
        "lng_asset_name",
        "lng_equipment_category",
        "telemetry_record_count",
        "avg_voltage",
        "avg_rotate",
        "avg_pressure",
        "avg_vibration",
        "error_count",
        "maintenance_event_count",
        "failure_count",
        "last_failure_type",
        "estimated_downtime_hours",
        "mtbf_style_hours",
        "mttr_style_hours",
        "availability_style_percent",
        "asset_health_score",
        "maintenance_priority",
        "engineering_note",
    ]

    return summary[output_columns].sort_values("machineID")


def build_report(summary: pd.DataFrame) -> str:
    """Create a Markdown report that explains the generated summary table."""
    priority_counts = (
        summary["maintenance_priority"].value_counts().sort_index().to_dict()
    )
    priority_lines = [
        f"- {priority}: {count}" for priority, count in priority_counts.items()
    ]

    return "\n".join(
        [
            "# Azure Reliability Summary Report",
            "",
            "## What The Script Does",
            "",
            "`scripts/build_azure_reliability_summary.py` reads the public Azure "
            "Predictive Maintenance dataset and builds one dashboard-ready "
            "reliability summary row per machine. The output is written to "
            "`data/processed/azure_machine_reliability_summary.csv`, and a "
            "GitHub-safe sample is written to "
            "`samples/azure/azure_machine_reliability_summary_sample.csv`.",
            "",
            "The Azure machines are mapped into LNG-style equipment categories "
            "for portfolio demonstration. This is an adapted public dataset; it "
            "does not use ExxonMobil, PNG LNG, confidential, proprietary, or "
            "licensee data.",
            "",
            "## Source Files Used",
            "",
            "- `data/raw/extracted/azure_pdm/PdM_machines.csv`",
            "- `data/raw/extracted/azure_pdm/PdM_telemetry.csv`",
            "- `data/raw/extracted/azure_pdm/PdM_errors.csv`",
            "- `data/raw/extracted/azure_pdm/PdM_failures.csv`",
            "- `data/raw/extracted/azure_pdm/PdM_maint.csv`",
            "",
            "The script reads these files only. It does not modify raw data.",
            "",
            "## Reliability KPIs Calculated",
            "",
            "- Telemetry record count as an operating-hour proxy",
            "- Average voltage, rotation, pressure, and vibration",
            "- Error count",
            "- Maintenance event count",
            "- Failure count",
            "- Last recorded failure type",
            "- Estimated downtime hours",
            "- MTBF-style hours",
            "- MTTR-style hours",
            "- Availability-style percent",
            "- Asset health score",
            "- Maintenance priority",
            "- Engineering note",
            "",
            "## Assumptions Used",
            "",
            "- Each failure is assumed to cause 8 downtime hours.",
            "- Telemetry record count is used as a simple operating-hour proxy.",
            "- MTBF-style estimate equals telemetry record count divided by "
            "failure count when failures exist.",
            "- MTTR-style estimate equals estimated downtime divided by failure "
            "count when failures exist.",
            "- Availability-style estimate uses telemetry records as the operating "
            "basis and estimated downtime as unavailable time.",
            "- Asset health score starts at 100 and subtracts points for failures, "
            "errors, maintenance events, and above-average vibration.",
            "- LNG-style asset IDs and equipment categories are demonstration "
            "mappings applied to public Azure machines.",
            "",
            "## Dashboard Usefulness",
            "",
            "This table gives the LNG Operations Technical Reliability Dashboard a "
            "first machine-level reliability layer. It can support dashboard "
            "views for asset ranking, maintenance priority filtering, health "
            "score comparison, and quick review of repeated failures or high "
            "sensor averages.",
            "",
            "## Limitations",
            "",
            "- These are MTBF-style, MTTR-style, and availability-style estimates, "
            "not formal plant reliability calculations.",
            "- The Azure dataset is public predictive maintenance data, not LNG "
            "plant operating history.",
            "- The LNG equipment categories are adapted labels for portfolio use.",
            "- Downtime is estimated with a fixed 8-hour assumption per failure.",
            "- Telemetry row count is only a proxy for operating hours.",
            "- The health score is a simple screening score, not a validated risk "
            "model.",
            "",
            "## Output Snapshot",
            "",
            f"- Machine rows created: {len(summary)}",
            f"- Average asset health score: {summary['asset_health_score'].mean():.1f}",
            f"- Minimum asset health score: {summary['asset_health_score'].min():.1f}",
            f"- Maximum asset health score: {summary['asset_health_score'].max():.1f}",
            "- Maintenance priority counts:",
            *priority_lines,
            "",
        ]
    )


def main() -> None:
    """Build all reliability summary outputs."""
    print("Building Azure machine reliability summary...")
    print(f"Project root: {PROJECT_ROOT}")

    check_required_files()
    summary = build_summary_table()

    PROCESSED_OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    SAMPLE_OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    REPORT_OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)

    summary.to_csv(PROCESSED_OUTPUT_PATH, index=False)
    summary.head(SAMPLE_ROW_LIMIT).to_csv(SAMPLE_OUTPUT_PATH, index=False)
    REPORT_OUTPUT_PATH.write_text(build_report(summary), encoding="utf-8")

    print()
    print("Reliability summary build complete.")
    print(f"Processed output written: {PROCESSED_OUTPUT_PATH.relative_to(PROJECT_ROOT)}")
    print(f"Sample output written: {SAMPLE_OUTPUT_PATH.relative_to(PROJECT_ROOT)}")
    print(f"Report written: {REPORT_OUTPUT_PATH.relative_to(PROJECT_ROOT)}")
    print(f"Machine rows created: {len(summary)}")


if __name__ == "__main__":
    main()
