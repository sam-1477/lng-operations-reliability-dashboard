"""
Profile the public MetroPT-3 compressor dataset.

This script reads the extracted MetroPT-3 compressor CSV from data/raw/. It is
read-only for raw data: it does not delete, edit, or overwrite the raw ZIP or
the extracted raw CSV file.

Outputs:
- reports/metropt3_data_profile.md
- samples/metropt3/metropt3_compressor_sample.csv

Run from the project root:
    python scripts\\inspect_metropt3_compressor.py
"""

from __future__ import annotations

import math
from pathlib import Path

try:
    import pandas as pd
except ImportError as error:
    raise SystemExit(
        "This script requires pandas. Install project dependencies with: "
        "pip install -r requirements.txt"
    ) from error


PROJECT_ROOT = Path(__file__).resolve().parents[1]
RAW_DATA_ROOT = PROJECT_ROOT / "data" / "raw"
METROPT3_EXTRACTED_DIR = RAW_DATA_ROOT / "extracted" / "metropt3"
REPORT_OUTPUT_PATH = PROJECT_ROOT / "reports" / "metropt3_data_profile.md"
SAMPLE_OUTPUT_PATH = (
    PROJECT_ROOT / "samples" / "metropt3" / "metropt3_compressor_sample.csv"
)

SAMPLE_ROW_LIMIT = 1000
PREVIEW_ROW_LIMIT = 5

# A chunk size of 100,000 rows keeps memory use modest while still running
# quickly on a laptop. The full CSV is large, so the script avoids reading the
# whole file into memory for row counts, missing values, and numeric summaries.
CHUNK_SIZE = 100_000


def find_raw_zip_files() -> list[Path]:
    """Find likely MetroPT-3 ZIP files for helpful error messages."""
    zip_candidates = []
    for pattern in ["*metropt*.zip", "*MetroPT*.zip", "*metropt*3*.zip"]:
        zip_candidates.extend(RAW_DATA_ROOT.rglob(pattern))
    return sorted(set(zip_candidates))


def clean_column_names(dataframe: pd.DataFrame) -> pd.DataFrame:
    """
    Give the raw unnamed row-index column a readable name.

    The raw CSV starts with a blank first column. Pandas reads this as
    "Unnamed: 0". Renaming it makes the report and sample easier to understand
    without changing the raw source file.
    """
    renamed_columns = {}
    unnamed_count = 0

    for column in dataframe.columns:
        column_text = str(column)
        if column_text.startswith("Unnamed"):
            unnamed_count += 1
            if unnamed_count == 1:
                renamed_columns[column] = "source_row_index"
            else:
                renamed_columns[column] = f"source_unnamed_{unnamed_count}"

    if renamed_columns:
        return dataframe.rename(columns=renamed_columns)

    return dataframe


def find_main_compressor_csv() -> Path:
    """
    Locate the main MetroPT-3 compressor CSV after extraction.

    The expected location is data/raw/extracted/metropt3/. If several CSV files
    are present, the largest compressor-named CSV is treated as the main file.
    """
    search_roots = [
        METROPT3_EXTRACTED_DIR,
        RAW_DATA_ROOT / "extracted",
    ]

    csv_candidates: list[Path] = []
    for root in search_roots:
        if root.exists():
            csv_candidates.extend(root.rglob("*.csv"))

    compressor_candidates = [
        path
        for path in csv_candidates
        if "compressor" in path.name.lower() or "aircompressor" in path.name.lower()
    ]

    if compressor_candidates:
        return max(compressor_candidates, key=lambda path: path.stat().st_size)

    if csv_candidates:
        return max(csv_candidates, key=lambda path: path.stat().st_size)

    zip_files = find_raw_zip_files()
    print("MetroPT-3 extracted compressor CSV was not found.")
    if zip_files:
        print("Likely raw ZIP file(s) found:")
        for path in zip_files:
            print(f"- {path.relative_to(PROJECT_ROOT)}")
        print(
            "Extract the MetroPT-3 ZIP into data/raw/extracted/metropt3/ "
            "and rerun this script."
        )
    else:
        print("No likely MetroPT-3 ZIP file was found under data/raw/.")

    raise SystemExit("Cannot profile MetroPT-3 until the compressor CSV is extracted.")


def get_preview_rows(csv_path: Path) -> pd.DataFrame:
    """Read a small preview from the main compressor CSV."""
    preview = pd.read_csv(csv_path, nrows=PREVIEW_ROW_LIMIT)
    return clean_column_names(preview)


def write_sample_file(csv_path: Path) -> pd.DataFrame:
    """Write a GitHub-safe sample capped at 1,000 rows."""
    sample = pd.read_csv(csv_path, nrows=SAMPLE_ROW_LIMIT)
    sample = clean_column_names(sample)

    SAMPLE_OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    sample.to_csv(SAMPLE_OUTPUT_PATH, index=False)
    return sample


def initialize_numeric_stats(columns: list[str]) -> dict[str, dict[str, float]]:
    """Create running-stat containers for numeric sensor columns."""
    return {
        column: {
            "count": 0.0,
            "sum": 0.0,
            "sum_squares": 0.0,
            "min": math.inf,
            "max": -math.inf,
        }
        for column in columns
    }


def update_numeric_stats(
    stats: dict[str, dict[str, float]], chunk: pd.DataFrame, numeric_columns: list[str]
) -> None:
    """Update count, mean ingredients, min, and max from one data chunk."""
    for column in numeric_columns:
        values = pd.to_numeric(chunk[column], errors="coerce").dropna()

        if values.empty:
            continue

        column_stats = stats[column]
        column_stats["count"] += float(values.count())
        column_stats["sum"] += float(values.sum())
        column_stats["sum_squares"] += float((values * values).sum())
        column_stats["min"] = min(column_stats["min"], float(values.min()))
        column_stats["max"] = max(column_stats["max"], float(values.max()))


def finalize_numeric_stats(stats: dict[str, dict[str, float]]) -> pd.DataFrame:
    """Convert running numeric stats into a readable summary table."""
    rows = []

    for column, column_stats in stats.items():
        count = column_stats["count"]

        if count == 0:
            rows.append(
                {
                    "column": column,
                    "count": 0,
                    "mean": None,
                    "std": None,
                    "min": None,
                    "max": None,
                }
            )
            continue

        mean = column_stats["sum"] / count
        if count > 1:
            variance = (
                column_stats["sum_squares"] - (column_stats["sum"] ** 2 / count)
            ) / (count - 1)
            std = math.sqrt(max(0.0, variance))
        else:
            std = 0.0

        rows.append(
            {
                "column": column,
                "count": int(count),
                "mean": round(mean, 4),
                "std": round(std, 4),
                "min": round(column_stats["min"], 4),
                "max": round(column_stats["max"], 4),
            }
        )

    return pd.DataFrame(rows)


def profile_csv(csv_path: Path) -> dict:
    """Profile the large compressor CSV using pandas chunks."""
    first_chunk = pd.read_csv(csv_path, nrows=CHUNK_SIZE)
    first_chunk = clean_column_names(first_chunk)

    columns = list(first_chunk.columns)
    numeric_columns = list(first_chunk.select_dtypes(include="number").columns)

    # source_row_index is an original row index, not a compressor sensor.
    sensor_columns = [
        column for column in numeric_columns if column != "source_row_index"
    ]

    missing_counts = pd.Series(0, index=columns, dtype="int64")
    numeric_stats = initialize_numeric_stats(sensor_columns)
    row_count = 0

    print("Streaming through the compressor CSV in chunks...")
    for chunk_number, chunk in enumerate(
        pd.read_csv(csv_path, chunksize=CHUNK_SIZE), start=1
    ):
        chunk = clean_column_names(chunk)
        row_count += len(chunk)
        missing_counts = missing_counts.add(chunk.isna().sum(), fill_value=0).astype(
            "int64"
        )
        update_numeric_stats(numeric_stats, chunk, sensor_columns)

        if chunk_number % 10 == 0:
            print(f"  Processed {row_count:,} rows...")

    missing_summary = pd.DataFrame(
        {
            "column": missing_counts.index,
            "missing_count": missing_counts.values,
            "missing_percent": [
                round((count / row_count) * 100, 4) if row_count else 0
                for count in missing_counts.values
            ],
        }
    )

    numeric_summary = finalize_numeric_stats(numeric_stats)

    return {
        "row_count": row_count,
        "columns": columns,
        "sensor_columns": sensor_columns,
        "missing_summary": missing_summary,
        "numeric_summary": numeric_summary,
    }


def dataframe_to_text(dataframe: pd.DataFrame, max_rows: int | None = None) -> str:
    """Format a dataframe as readable plain text for terminal and Markdown."""
    if dataframe.empty:
        return "(no rows)"

    if max_rows is not None:
        dataframe = dataframe.head(max_rows)

    return dataframe.to_string(index=False)


def build_report(csv_path: Path, preview: pd.DataFrame, profile: dict) -> str:
    """Create the Markdown data-profile report."""
    relative_csv_path = csv_path.relative_to(PROJECT_ROOT)
    relative_sample_path = SAMPLE_OUTPUT_PATH.relative_to(PROJECT_ROOT)

    return "\n".join(
        [
            "# MetroPT-3 Compressor Data Profile",
            "",
            "This report profiles the public MetroPT-3 compressor dataset for "
            "portfolio demonstration. The dataset is adapted for LNG-style "
            "compressor surveillance and rotating equipment health monitoring.",
            "",
            "This is a public compressor dataset. It is not ExxonMobil or PNG "
            "LNG operating data, and it does not contain confidential, "
            "proprietary, or licensee data.",
            "",
            "## Main Compressor File",
            "",
            f"- File name: `{csv_path.name}`",
            f"- Source path: `{relative_csv_path.as_posix()}`",
            f"- Row count: {profile['row_count']:,}",
            f"- Column count: {len(profile['columns'])}",
            f"- GitHub-safe sample: `{relative_sample_path.as_posix()}`",
            "",
            "## Column Names",
            "",
            "The raw CSV contains a blank first column that is labeled "
            "`source_row_index` in this profile and sample.",
            "",
            "```text",
            ", ".join(profile["columns"]),
            "```",
            "",
            f"## First {PREVIEW_ROW_LIMIT} Rows",
            "",
            "```text",
            dataframe_to_text(preview),
            "```",
            "",
            "## Missing Value Summary",
            "",
            "```text",
            dataframe_to_text(profile["missing_summary"]),
            "```",
            "",
            "## Basic Numeric Summary For Sensor Columns",
            "",
            "The numeric summary is calculated in chunks to avoid loading the "
            "full 218 MB CSV into memory unnecessarily.",
            "",
            "```text",
            dataframe_to_text(profile["numeric_summary"]),
            "```",
            "",
            "## Useful Compressor Surveillance Columns",
            "",
            "- `TP2`, `TP3`, `H1`, `DV_pressure`, and `Reservoirs` can support "
            "pressure trend and pressure alert views.",
            "- `Oil_temperature` can support oil temperature monitoring and "
            "high-temperature alert counts.",
            "- `Motor_current` can support compressor load and running-state "
            "surveillance.",
            "- `COMP`, `DV_eletric`, `Towers`, `MPG`, `LPS`, `Pressure_switch`, "
            "`Oil_level`, and `Caudal_impulses` can support operating-status "
            "and signal-state checks.",
            "",
            "## Notes",
            "",
            "- Raw MetroPT-3 files remain local under `data/raw/`.",
            "- This script writes only the Markdown profile and small sample CSV.",
            f"- The sample file is capped at {SAMPLE_ROW_LIMIT:,} rows.",
            "- The data is adapted for LNG-style compressor surveillance as a "
            "portfolio demonstration.",
            "",
        ]
    )


def print_profile(csv_path: Path, preview: pd.DataFrame, profile: dict) -> None:
    """Print the requested profile details to the terminal."""
    print()
    print("MetroPT-3 compressor data profile")
    print(f"File name: {csv_path.name}")
    print(f"Path: {csv_path.relative_to(PROJECT_ROOT)}")
    print(f"Row count: {profile['row_count']:,}")
    print("Column names:")
    print(", ".join(profile["columns"]))
    print()
    print(f"First {PREVIEW_ROW_LIMIT} rows:")
    print(dataframe_to_text(preview))
    print()
    print("Missing value summary:")
    print(dataframe_to_text(profile["missing_summary"]))
    print()
    print("Basic numeric summary for sensor columns:")
    print(dataframe_to_text(profile["numeric_summary"]))


def main() -> None:
    """Run the MetroPT-3 profiling workflow."""
    print("Inspecting MetroPT-3 compressor dataset...")
    print(f"Project root: {PROJECT_ROOT}")
    print(f"Expected extracted folder: {METROPT3_EXTRACTED_DIR}")

    csv_path = find_main_compressor_csv()
    print(f"Main compressor CSV identified: {csv_path.relative_to(PROJECT_ROOT)}")

    preview = get_preview_rows(csv_path)
    sample = write_sample_file(csv_path)
    profile = profile_csv(csv_path)

    REPORT_OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    REPORT_OUTPUT_PATH.write_text(
        build_report(csv_path, preview, profile), encoding="utf-8"
    )

    print_profile(csv_path, preview, profile)

    print()
    print("MetroPT-3 profiling complete.")
    print(f"Report written: {REPORT_OUTPUT_PATH.relative_to(PROJECT_ROOT)}")
    print(f"Sample written: {SAMPLE_OUTPUT_PATH.relative_to(PROJECT_ROOT)}")
    print(f"Sample rows written: {len(sample):,}")


if __name__ == "__main__":
    main()
