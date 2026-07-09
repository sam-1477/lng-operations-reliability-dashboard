"""
Profile the public Azure Predictive Maintenance dataset.

This script is intentionally read-only for files in data/raw/. It looks for the
five Azure PdM CSV files, prints a small profile to the terminal, writes a
Markdown report, and creates small sample CSV files for GitHub.

Run from the project root:
    python scripts\\inspect_azure_pdm.py
"""

from __future__ import annotations

import csv
from pathlib import Path

try:
    import pandas as pd
except ImportError as error:
    raise SystemExit(
        "This script requires pandas. Install project dependencies with: "
        "pip install -r requirements.txt"
    ) from error


# Locate important project folders from this script's location.
PROJECT_ROOT = Path(__file__).resolve().parents[1]
RAW_DATA_ROOT = PROJECT_ROOT / "data" / "raw"
RAW_EXTRACTED_ROOT = RAW_DATA_ROOT / "extracted"
REPORT_PATH = PROJECT_ROOT / "reports" / "azure_data_profile.md"
SAMPLE_OUTPUT_DIR = PROJECT_ROOT / "samples" / "azure"

# Keep GitHub samples small.
PREVIEW_ROW_LIMIT = 5
SAMPLE_ROW_LIMIT = 100

# Expected Azure Predictive Maintenance files.
AZURE_FILE_NAMES = [
    "PdM_machines.csv",
    "PdM_telemetry.csv",
    "PdM_errors.csv",
    "PdM_failures.csv",
    "PdM_maint.csv",
]


def find_azure_file(file_name: str) -> Path | None:
    """Find an Azure CSV without extracting or modifying raw data."""
    likely_locations = [
        RAW_EXTRACTED_ROOT / "azure_pdm" / file_name,
        RAW_EXTRACTED_ROOT / file_name,
        RAW_DATA_ROOT / "azure_pdm" / file_name,
    ]

    for candidate in likely_locations:
        if candidate.exists():
            return candidate

    # Fallback: search under data/raw/ in case the extracted folder is named
    # differently on another machine.
    if RAW_DATA_ROOT.exists():
        matches = sorted(RAW_DATA_ROOT.rglob(file_name))
        if matches:
            return matches[0]

    return None


def count_data_rows(csv_path: Path) -> int:
    """Count CSV data rows, excluding the header row."""
    with csv_path.open("r", encoding="utf-8-sig", newline="") as csv_file:
        reader = csv.reader(csv_file)
        next(reader, None)  # Skip header.
        return sum(1 for _ in reader)


def read_first_rows(csv_path: Path, row_limit: int) -> pd.DataFrame:
    """Read only the first few rows for preview or sampling."""
    return pd.read_csv(csv_path, nrows=row_limit)


def write_sample_csv(source_path: Path) -> Path:
    """Write a small sample CSV outside data/raw/."""
    SAMPLE_OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    sample_path = SAMPLE_OUTPUT_DIR / f"{source_path.stem}_sample.csv"
    sample = read_first_rows(source_path, SAMPLE_ROW_LIMIT)
    sample.to_csv(sample_path, index=False)
    return sample_path


def format_preview_table(preview: pd.DataFrame) -> str:
    """Format preview rows for both terminal output and Markdown."""
    if preview.empty:
        return "(no rows)"

    return preview.to_string(index=False)


def build_report(profiles: list[dict], missing_files: list[str]) -> str:
    """Create the Markdown report text."""
    lines = [
        "# Azure Predictive Maintenance Data Profile",
        "",
        "This report profiles the public Microsoft Azure Predictive Maintenance "
        "dataset files found locally. The data is used as a public industrial "
        "reliability dataset and may be adapted into LNG-style reliability "
        "categories later in the project.",
        "",
        "No ExxonMobil, PNG LNG, confidential, proprietary, or licensee data is "
        "used in this profile.",
        "",
        "## Source Files",
        "",
        "| File | Status | Rows | Columns | Sample Output |",
        "|---|---:|---:|---:|---|",
    ]

    for profile in profiles:
        relative_sample = profile["sample_path"].relative_to(PROJECT_ROOT)
        lines.append(
            f"| `{profile['file_name']}` | found | {profile['row_count']} | "
            f"{len(profile['columns'])} | `{relative_sample.as_posix()}` |"
        )

    for file_name in missing_files:
        lines.append(f"| `{file_name}` | missing |  |  |  |")

    if missing_files:
        lines.extend(
            [
                "",
                "## Missing Files",
                "",
                "The missing files were not extracted when this report was generated. "
                "Place the Azure PdM CSV files in `data/raw/extracted/azure_pdm/` "
                "and rerun `python scripts\\inspect_azure_pdm.py`.",
            ]
        )

    lines.extend(["", "## File Details", ""])

    for profile in profiles:
        relative_source = profile["source_path"].relative_to(PROJECT_ROOT)
        lines.extend(
            [
                f"### {profile['file_name']}",
                "",
                f"- Source path: `{relative_source.as_posix()}`",
                f"- Row count: {profile['row_count']}",
                f"- Columns: {', '.join(profile['columns'])}",
                "",
                f"First {PREVIEW_ROW_LIMIT} rows:",
                "",
                "```text",
                format_preview_table(profile["preview"]),
                "```",
                "",
            ]
        )

    lines.extend(
        [
            "## Notes",
            "",
            "- Raw data remains local under `data/raw/` and is not modified by this script.",
            f"- Sample CSV files are capped at {SAMPLE_ROW_LIMIT} rows each.",
            "- The generated samples are for portfolio demonstration and repository review only.",
            "",
        ]
    )

    return "\n".join(lines)


def main() -> None:
    profiles: list[dict] = []
    missing_files: list[str] = []

    print("Azure Predictive Maintenance dataset profile")
    print(f"Project root: {PROJECT_ROOT}")
    print(f"Looking under: {RAW_DATA_ROOT}")
    print()

    for file_name in AZURE_FILE_NAMES:
        source_path = find_azure_file(file_name)

        if source_path is None:
            missing_files.append(file_name)
            print(f"{file_name}: missing")
            print()
            continue

        row_count = count_data_rows(source_path)
        preview = read_first_rows(source_path, PREVIEW_ROW_LIMIT)
        sample_path = write_sample_csv(source_path)

        profile = {
            "file_name": file_name,
            "source_path": source_path,
            "row_count": row_count,
            "columns": list(preview.columns),
            "preview": preview,
            "sample_path": sample_path,
        }
        profiles.append(profile)

        print(f"File: {file_name}")
        print(f"Path: {source_path.relative_to(PROJECT_ROOT)}")
        print(f"Rows: {row_count}")
        print(f"Columns: {', '.join(profile['columns'])}")
        print(f"First {PREVIEW_ROW_LIMIT} rows:")
        print(format_preview_table(preview))
        print(f"Sample written: {sample_path.relative_to(PROJECT_ROOT)}")
        print()

    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    REPORT_PATH.write_text(build_report(profiles, missing_files), encoding="utf-8")

    print(f"Report written: {REPORT_PATH.relative_to(PROJECT_ROOT)}")
    print(f"Sample folder: {SAMPLE_OUTPUT_DIR.relative_to(PROJECT_ROOT)}")

    if missing_files:
        print()
        print("Missing Azure files:")
        for file_name in missing_files:
            print(f"- {file_name}")


if __name__ == "__main__":
    main()
