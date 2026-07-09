"""
Inspect public PHMSA LNG and Gas Transmission incident datasets.

This script reads extracted PHMSA files from data/raw/. It does not delete,
edit, or overwrite raw ZIP files or extracted raw files.

Outputs:
- reports/phmsa_incident_data_profile.md
- reports/phmsa_incident_risk_summary_report.md
- data/processed/phmsa_incident_risk_summary.csv
- samples/phmsa/phmsa_lng_incident_sample.csv
- samples/phmsa/phmsa_gas_transmission_incident_sample.csv

Run from the project root:
    python scripts\\inspect_phmsa_incidents.py
"""

from __future__ import annotations

import zipfile
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
PROCESSED_OUTPUT_PATH = (
    PROJECT_ROOT / "data" / "processed" / "phmsa_incident_risk_summary.csv"
)
PROFILE_REPORT_PATH = PROJECT_ROOT / "reports" / "phmsa_incident_data_profile.md"
RISK_REPORT_PATH = PROJECT_ROOT / "reports" / "phmsa_incident_risk_summary_report.md"
SAMPLE_OUTPUT_DIR = PROJECT_ROOT / "samples" / "phmsa"

SAMPLE_ROW_LIMIT = 500
PREVIEW_ROW_LIMIT = 5

DATASETS = [
    {
        "name": "PHMSA LNG Incidents",
        "short_name": "phmsa_lng",
        "zip_path": RAW_DATA_ROOT / "phmsa_lng_incident_data_2011_present.zip",
        "extracted_dir": RAW_DATA_ROOT / "extracted" / "phmsa_lng",
        "sample_path": SAMPLE_OUTPUT_DIR / "phmsa_lng_incident_sample.csv",
    },
    {
        "name": "PHMSA Gas Transmission Incidents",
        "short_name": "phmsa_gas_transmission",
        "zip_path": RAW_DATA_ROOT
        / "phmsa_gas_transmission_incident_data_2010_present.zip",
        "extracted_dir": RAW_DATA_ROOT / "extracted" / "phmsa_gas_transmission",
        "sample_path": SAMPLE_OUTPUT_DIR
        / "phmsa_gas_transmission_incident_sample.csv",
    },
]

# These candidate lists make the script resilient to PHMSA column-name changes.
# The script tries exact matches first. If none are found, it looks for useful
# keyword combinations in the available columns.
FIELD_CANDIDATES = {
    "year": {
        "label": "year",
        "candidates": ["IYEAR", "INCIDENT_YEAR", "YEAR"],
        "keywords": [["YEAR"]],
    },
    "state": {
        "label": "state_or_location_field_if_available",
        "candidates": [
            "FACILITY_STATE",
            "ONSHORE_STATE_ABBREVIATION",
            "OFFSHORE_STATE_ABBREVIATION",
            "OPERATOR_STATE_ABBREVIATION",
            "LOCATION_STATE",
            "STATE",
        ],
        "keywords": [["STATE"]],
    },
    "cause": {
        "label": "cause_category_if_available",
        "candidates": [
            "CAUSE",
            "ROOT_CAUSE_CATEGORY",
            "ROOT_CAUSE_TYPE",
            "CAUSE_DETAILS",
        ],
        "keywords": [["CAUSE"]],
    },
    "incident_type": {
        "label": "incident_type_or_system_type_if_available",
        "candidates": [
            "PIPELINE_FUNCTION",
            "PIPE_FACILITY_TYPE",
            "SYSTEM_PART_INVOLVED",
            "ITEM_INVOLVED",
            "FACILITY_STATUS",
            "LOCATION_TYPE",
        ],
        "keywords": [["PIPELINE", "FUNCTION"], ["SYSTEM", "PART"], ["ITEM"]],
    },
    "cost": {
        "label": "total_estimated_cost_if_available",
        "candidates": [
            "PRPTY",
            "TOTAL_ESTIMATED_COST",
            "TOTAL_COST",
            "EST_COST_TOTAL",
            "ESTIMATED_TOTAL_COST",
        ],
        "keywords": [["TOTAL", "COST"], ["PRPTY"]],
    },
    "fatalities": {
        "label": "fatalities_if_available",
        "candidates": ["FATAL", "FATALITIES", "TOTAL_FATALITIES"],
        "keywords": [["FATAL"]],
    },
    "injuries": {
        "label": "injuries_if_available",
        "candidates": ["INJURE", "INJURIES", "TOTAL_INJURIES"],
        "keywords": [["INJUR"]],
    },
    "ignition": {
        "label": "ignition_or_fire_field_if_available",
        "candidates": ["IGNITE_IND", "FIRE_IND", "EXPLODE_IND"],
        "keywords": [["IGNITE"], ["FIRE"]],
    },
    "release": {
        "label": "release_or_leak_field_if_available",
        "candidates": [
            "RELEASE_TYPE",
            "COMMODITY_RELEASED_TYPE",
            "UNINTENTIONAL_RELEASE_IND",
            "UNINTENTIONAL_RELEASE",
            "LEAK_TYPE",
        ],
        "keywords": [["RELEASE"], ["LEAK"]],
    },
}


def normalize_column_name(column_name: str) -> str:
    """Normalize a column name for matching."""
    return "".join(character for character in column_name.upper() if character.isalnum())


def make_unique_column_names(columns: list[str]) -> list[str]:
    """Avoid duplicate column names after cleaning."""
    counts: dict[str, int] = {}
    unique_columns = []

    for column in columns:
        if column not in counts:
            counts[column] = 1
            unique_columns.append(column)
        else:
            counts[column] += 1
            unique_columns.append(f"{column}_{counts[column]}")

    return unique_columns


def clean_dataframe(dataframe: pd.DataFrame) -> pd.DataFrame:
    """
    Clean column names in the copied dataframe.

    PHMSA Gas Transmission files can contain trailing blank columns. The script
    drops blank unnamed columns when they contain no values. This only affects
    the derived sample/report dataframes, not the raw files.
    """
    cleaned_columns = []
    unnamed_count = 0

    for column in dataframe.columns:
        column_text = str(column).strip()
        if column_text == "" or column_text.lower().startswith("unnamed"):
            unnamed_count += 1
            column_text = f"source_unnamed_{unnamed_count}"
        cleaned_columns.append(column_text)

    dataframe = dataframe.copy()
    dataframe.columns = make_unique_column_names(cleaned_columns)

    empty_unnamed_columns = []
    for column in dataframe.columns:
        if not column.startswith("source_unnamed_"):
            continue

        values = dataframe[column].astype(str).str.strip()
        if values.eq("").all() or values.str.lower().eq("nan").all():
            empty_unnamed_columns.append(column)

    if empty_unnamed_columns:
        dataframe = dataframe.drop(columns=empty_unnamed_columns)

    return dataframe


def safely_extract_zip(zip_path: Path, destination: Path) -> None:
    """
    Extract a PHMSA ZIP only when the extracted data file is missing.

    This keeps extraction constrained to the approved data/raw/extracted/
    dataset folder and protects against unexpected path traversal entries.
    """
    destination.mkdir(parents=True, exist_ok=True)
    destination_resolved = destination.resolve()

    with zipfile.ZipFile(zip_path) as zip_file:
        for member in zip_file.infolist():
            target_path = (destination / member.filename).resolve()
            if not str(target_path).startswith(str(destination_resolved)):
                raise SystemExit(f"Unsafe ZIP entry blocked: {member.filename}")
        zip_file.extractall(destination)


def ensure_extracted_files(dataset: dict) -> None:
    """Extract a dataset only if no text/CSV data files are already present."""
    extracted_dir = dataset["extracted_dir"]
    data_files = find_data_files(extracted_dir)

    if data_files:
        return

    zip_path = dataset["zip_path"]
    if not zip_path.exists():
        raise SystemExit(
            f"{dataset['name']} is missing. Expected ZIP: "
            f"{zip_path.relative_to(PROJECT_ROOT)}"
        )

    print(
        f"No extracted data file found for {dataset['name']}. "
        f"Extracting {zip_path.relative_to(PROJECT_ROOT)}..."
    )
    safely_extract_zip(zip_path, extracted_dir)


def find_data_files(folder: Path) -> list[Path]:
    """Find likely PHMSA data files in an extracted folder."""
    if not folder.exists():
        return []

    data_files = []
    for extension in ("*.txt", "*.csv"):
        data_files.extend(folder.rglob(extension))

    return sorted(data_files)


def find_dictionary_files(folder: Path) -> list[Path]:
    """Find likely PHMSA codebook or data dictionary files."""
    if not folder.exists():
        return []

    dictionary_files = []
    for extension in ("*.pdf", "*.xlsx", "*.xls", "*.docx"):
        dictionary_files.extend(folder.rglob(extension))

    return sorted(dictionary_files)


def select_main_data_file(data_files: list[Path]) -> Path:
    """Use the largest text/CSV file as the main incident data file."""
    if not data_files:
        raise SystemExit("No PHMSA data files were found after extraction.")
    return max(data_files, key=lambda path: path.stat().st_size)


def read_phmsa_file(file_path: Path) -> pd.DataFrame:
    """
    Read a PHMSA tab-delimited text file.

    Values are loaded as strings first. Numeric fields are converted only when
    needed for the risk summary, which keeps the import predictable for a
    beginner-friendly workflow.
    """
    encodings_to_try = ["utf-8-sig", "cp1252"]

    for encoding in encodings_to_try:
        try:
            dataframe = pd.read_csv(
                file_path,
                sep="\t",
                dtype=str,
                keep_default_na=False,
                encoding=encoding,
                low_memory=False,
            )
            return clean_dataframe(dataframe)
        except UnicodeDecodeError:
            continue

    raise SystemExit(f"Could not read {file_path} with the expected encodings.")


def select_best_column(columns: list[str], field_key: str) -> str | None:
    """Select the best available column for a logical risk-summary field."""
    field_config = FIELD_CANDIDATES[field_key]
    normalized_lookup = {
        normalize_column_name(column): column for column in columns
    }

    for candidate in field_config["candidates"]:
        normalized_candidate = normalize_column_name(candidate)
        if normalized_candidate in normalized_lookup:
            return normalized_lookup[normalized_candidate]

    for keyword_group in field_config["keywords"]:
        normalized_keywords = [normalize_column_name(keyword) for keyword in keyword_group]
        for column in columns:
            normalized_column = normalize_column_name(column)
            if all(keyword in normalized_column for keyword in normalized_keywords):
                return column

    return None


def selected_field_map(dataframe: pd.DataFrame) -> dict[str, str | None]:
    """Map logical field names to actual PHMSA columns where possible."""
    return {
        field_key: select_best_column(list(dataframe.columns), field_key)
        for field_key in FIELD_CANDIDATES
    }


def is_missing_value_series(series: pd.Series) -> pd.Series:
    """Treat blanks and common placeholder values as missing."""
    values = series.astype(str).str.strip()
    return values.eq("") | values.str.upper().isin(
        ["N/A", "NA", "NONE", "NULL", "NOT REPORTED"]
    )


def build_missing_summary(
    dataframe: pd.DataFrame, field_map: dict[str, str | None]
) -> pd.DataFrame:
    """Summarize missing values for the logical key fields."""
    rows = []
    row_count = len(dataframe)

    for field_key, selected_column in field_map.items():
        logical_label = FIELD_CANDIDATES[field_key]["label"]

        if selected_column is None:
            rows.append(
                {
                    "logical_field": logical_label,
                    "selected_column": "Not available",
                    "missing_count": "Not available",
                    "missing_percent": "Not available",
                }
            )
            continue

        missing_count = int(is_missing_value_series(dataframe[selected_column]).sum())
        missing_percent = round((missing_count / row_count) * 100, 2) if row_count else 0
        rows.append(
            {
                "logical_field": logical_label,
                "selected_column": selected_column,
                "missing_count": missing_count,
                "missing_percent": missing_percent,
            }
        )

    return pd.DataFrame(rows)


def clean_text_series(series: pd.Series, default_value: str = "Not available") -> pd.Series:
    """Return stripped text values with blanks replaced by a clear default."""
    cleaned = series.astype(str).str.strip()
    return cleaned.mask(cleaned.eq(""), default_value)


def get_text_field(
    dataframe: pd.DataFrame, selected_column: str | None, default_value: str = "Not available"
) -> pd.Series:
    """Get a text field or a default value if the field is unavailable."""
    if selected_column is None:
        return pd.Series([default_value] * len(dataframe), index=dataframe.index)
    return clean_text_series(dataframe[selected_column], default_value)


def get_numeric_field(dataframe: pd.DataFrame, selected_column: str | None) -> pd.Series:
    """Get a numeric field or zeros if the field is unavailable."""
    if selected_column is None:
        return pd.Series([0.0] * len(dataframe), index=dataframe.index)

    cleaned = (
        dataframe[selected_column]
        .astype(str)
        .str.replace("$", "", regex=False)
        .str.replace(",", "", regex=False)
        .str.strip()
    )
    return pd.to_numeric(cleaned, errors="coerce").fillna(0.0)


def yes_like(value: object) -> bool:
    """Identify simple yes/true indicator values."""
    text = str(value).strip().upper()
    return text in {"YES", "Y", "TRUE", "1"}


def build_dashboard_risk_note(row: pd.Series) -> str:
    """Create a short risk-awareness note for each grouped summary row."""
    cause_text = str(row["cause_category_if_available"]).upper()
    incident_type_text = str(row["incident_type_or_system_type_if_available"]).upper()
    release_text = str(row["release_or_leak_field_if_available"]).upper()

    if row["fatalities_if_available"] > 0 or row["injuries_if_available"] > 0:
        return (
            "Higher consequence group. Review injuries/fatalities and cause context; "
            "risk-awareness summary, not a formal integrity assessment."
        )

    if yes_like(row["ignition_or_fire_field_if_available"]) or "FIRE" in release_text:
        return (
            "Ignition or fire indicator present. Review emergency response and "
            "prevention themes."
        )

    if row["total_estimated_cost_if_available"] >= 1_000_000:
        return "High reported cost group. Review consequence severity and controls."

    if row["incident_count"] >= 10:
        return "Recurring incident group. Review trend for dashboard risk awareness."

    if any(
        keyword in cause_text or keyword in incident_type_text
        for keyword in ["CORROSION", "MATERIAL", "EQUIPMENT", "FAILURE", "WELD"]
    ):
        return "Mechanical integrity theme. Review cause category and asset context."

    return "Use for LNG-style incident risk awareness and trend review."


def normalize_dataset_for_summary(
    dataset_name: str, dataframe: pd.DataFrame, field_map: dict[str, str | None]
) -> pd.DataFrame:
    """Create standard incident rows before grouping."""
    normalized = pd.DataFrame(
        {
            "source_dataset": dataset_name,
            "year": get_text_field(dataframe, field_map["year"]),
            "state_or_location_field_if_available": get_text_field(
                dataframe, field_map["state"]
            ),
            "cause_category_if_available": get_text_field(
                dataframe, field_map["cause"]
            ),
            "incident_type_or_system_type_if_available": get_text_field(
                dataframe, field_map["incident_type"]
            ),
            "total_estimated_cost_if_available": get_numeric_field(
                dataframe, field_map["cost"]
            ),
            "fatalities_if_available": get_numeric_field(
                dataframe, field_map["fatalities"]
            ),
            "injuries_if_available": get_numeric_field(
                dataframe, field_map["injuries"]
            ),
            "ignition_or_fire_field_if_available": get_text_field(
                dataframe, field_map["ignition"]
            ),
            "release_or_leak_field_if_available": get_text_field(
                dataframe, field_map["release"]
            ),
        }
    )
    return normalized


def build_risk_summary(normalized_incidents: pd.DataFrame) -> pd.DataFrame:
    """Group incidents into a dashboard-ready risk-awareness summary."""
    group_columns = [
        "source_dataset",
        "year",
        "state_or_location_field_if_available",
        "cause_category_if_available",
        "incident_type_or_system_type_if_available",
        "ignition_or_fire_field_if_available",
        "release_or_leak_field_if_available",
    ]

    summary = (
        normalized_incidents.groupby(group_columns, dropna=False)
        .agg(
            incident_count=("source_dataset", "size"),
            total_estimated_cost_if_available=(
                "total_estimated_cost_if_available",
                "sum",
            ),
            fatalities_if_available=("fatalities_if_available", "sum"),
            injuries_if_available=("injuries_if_available", "sum"),
        )
        .reset_index()
    )

    # Round money-style and count-style values for cleaner CSV output.
    summary["total_estimated_cost_if_available"] = summary[
        "total_estimated_cost_if_available"
    ].round(2)
    summary["fatalities_if_available"] = summary["fatalities_if_available"].round(0).astype(
        int
    )
    summary["injuries_if_available"] = summary["injuries_if_available"].round(0).astype(
        int
    )

    summary["dashboard_risk_note"] = summary.apply(build_dashboard_risk_note, axis=1)

    output_columns = [
        "source_dataset",
        "incident_count",
        "year",
        "state_or_location_field_if_available",
        "cause_category_if_available",
        "incident_type_or_system_type_if_available",
        "total_estimated_cost_if_available",
        "fatalities_if_available",
        "injuries_if_available",
        "ignition_or_fire_field_if_available",
        "release_or_leak_field_if_available",
        "dashboard_risk_note",
    ]

    return summary[output_columns].sort_values(
        ["source_dataset", "year", "incident_count"],
        ascending=[True, True, False],
    )


def dataframe_to_text(dataframe: pd.DataFrame, max_rows: int | None = None) -> str:
    """Format dataframe output for terminal and Markdown."""
    if dataframe.empty:
        return "(no rows)"

    if max_rows is not None:
        dataframe = dataframe.head(max_rows)

    return dataframe.to_string(index=False)


def write_sample(dataframe: pd.DataFrame, sample_path: Path) -> int:
    """Write a GitHub-safe sample file with at most 500 rows."""
    sample_path.parent.mkdir(parents=True, exist_ok=True)
    sample = dataframe.head(SAMPLE_ROW_LIMIT)
    sample.to_csv(sample_path, index=False)
    return len(sample)


def profile_dataset(dataset: dict) -> dict:
    """Load one PHMSA dataset, profile it, and write its sample file."""
    ensure_extracted_files(dataset)

    extracted_dir = dataset["extracted_dir"]
    data_files = find_data_files(extracted_dir)
    dictionary_files = find_dictionary_files(extracted_dir)
    main_data_file = select_main_data_file(data_files)

    dataframe = read_phmsa_file(main_data_file)
    field_map = selected_field_map(dataframe)
    missing_summary = build_missing_summary(dataframe, field_map)
    sample_rows = write_sample(dataframe, dataset["sample_path"])

    profile = {
        "dataset": dataset,
        "data_files": data_files,
        "dictionary_files": dictionary_files,
        "main_data_file": main_data_file,
        "dataframe": dataframe,
        "row_count": len(dataframe),
        "columns": list(dataframe.columns),
        "preview": dataframe.head(PREVIEW_ROW_LIMIT),
        "field_map": field_map,
        "missing_summary": missing_summary,
        "sample_rows": sample_rows,
    }

    return profile


def field_map_to_dataframe(field_map: dict[str, str | None]) -> pd.DataFrame:
    """Convert selected field mappings to a small table."""
    rows = []
    for field_key, selected_column in field_map.items():
        rows.append(
            {
                "logical_field": FIELD_CANDIDATES[field_key]["label"],
                "selected_column": selected_column or "Not available",
            }
        )
    return pd.DataFrame(rows)


def build_profile_report(profiles: list[dict]) -> str:
    """Create the PHMSA incident data profile Markdown report."""
    lines = [
        "# PHMSA Incident Data Profile",
        "",
        "This report profiles public PHMSA incident data for LNG and gas "
        "transmission incident awareness. The data is adapted for LNG-style "
        "incident risk awareness as a portfolio demonstration.",
        "",
        "This is not ExxonMobil or PNG LNG operating data. It does not contain "
        "confidential, proprietary, or licensee data.",
        "",
    ]

    for profile in profiles:
        dataset = profile["dataset"]
        relative_main_file = profile["main_data_file"].relative_to(PROJECT_ROOT)
        relative_sample = dataset["sample_path"].relative_to(PROJECT_ROOT)
        data_file_names = ", ".join(path.name for path in profile["data_files"])
        dictionary_file_names = ", ".join(
            path.name for path in profile["dictionary_files"]
        )
        if not dictionary_file_names:
            dictionary_file_names = "Not available"

        # Wide PHMSA files are difficult to read in full-width previews. The
        # report includes the mapped dashboard fields for the first five rows,
        # while the sample CSV contains the full available columns.
        preview_columns = [
            column
            for column in profile["field_map"].values()
            if column is not None and column in profile["preview"].columns
        ]
        preview_columns = list(dict.fromkeys(preview_columns))
        preview = profile["preview"][preview_columns] if preview_columns else profile["preview"]

        lines.extend(
            [
                f"## {dataset['name']}",
                "",
                f"- Files found: {data_file_names}",
                f"- Data dictionary/description files found: {dictionary_file_names}",
                f"- Main data file selected: `{relative_main_file.as_posix()}`",
                f"- Row count: {profile['row_count']:,}",
                f"- Column count: {len(profile['columns'])}",
                f"- GitHub-safe sample: `{relative_sample.as_posix()}`",
                "",
                "### Column Names",
                "",
                "```text",
                ", ".join(profile["columns"]),
                "```",
                "",
                f"### First {PREVIEW_ROW_LIMIT} Rows For Mapped Key Fields",
                "",
                "```text",
                dataframe_to_text(preview),
                "```",
                "",
                "### Best-Effort Field Mapping",
                "",
                "```text",
                dataframe_to_text(field_map_to_dataframe(profile["field_map"])),
                "```",
                "",
                "### Missing Value Summary For Key Fields",
                "",
                "```text",
                dataframe_to_text(profile["missing_summary"]),
                "```",
                "",
            ]
        )

    lines.extend(
        [
            "## Notes",
            "",
            "- Raw PHMSA ZIP files and extracted raw files remain under `data/raw/`.",
            "- Sample CSV files are capped at 500 rows each.",
            "- The processed incident summary is a risk-awareness summary, not a "
            "formal integrity assessment.",
            "- PHMSA data is public US incident data adapted for LNG-style "
            "incident risk awareness and portfolio demonstration.",
            "",
        ]
    )

    return "\n".join(lines)


def build_risk_report(
    profiles: list[dict], risk_summary: pd.DataFrame, normalized_incidents: pd.DataFrame
) -> str:
    """Create the PHMSA risk-summary Markdown report."""
    source_counts = (
        normalized_incidents["source_dataset"].value_counts().sort_index().to_dict()
    )
    source_count_lines = [
        f"- {source_dataset}: {count:,}" for source_dataset, count in source_counts.items()
    ]

    field_sections = []
    for profile in profiles:
        field_sections.extend(
            [
                f"### {profile['dataset']['name']}",
                "",
                "```text",
                dataframe_to_text(field_map_to_dataframe(profile["field_map"])),
                "```",
                "",
            ]
        )

    return "\n".join(
        [
            "# PHMSA Incident Risk Summary Report",
            "",
            "## What The PHMSA Datasets Represent",
            "",
            "The PHMSA LNG incident dataset contains public incident records for "
            "US LNG facilities. The PHMSA Gas Transmission incident dataset "
            "contains public incident records for US gas transmission and "
            "gathering pipeline systems.",
            "",
            "For this project, the data is adapted for LNG-style incident risk "
            "awareness as a portfolio demonstration. It is not ExxonMobil or "
            "PNG LNG operating data.",
            "",
            "## Why This Helps The Dashboard",
            "",
            "Public PHMSA incident data gives the LNG Operations Technical "
            "Reliability Dashboard a credible public-data basis for incident "
            "awareness, pipeline incident trends, consequence severity, cause "
            "category review, and mechanical integrity context.",
            "",
            "Useful dashboard sections supported by this data include:",
            "",
            "- LNG incident awareness",
            "- Pipeline incident trends",
            "- Consequence severity",
            "- Cause category review",
            "- Mechanical integrity and risk context",
            "",
            "## Fields Available And Matched",
            "",
            *field_sections,
            "## Incident-Risk Summary Created",
            "",
            "The processed file "
            "`data/processed/phmsa_incident_risk_summary.csv` groups incidents "
            "by public dataset, year, location/state field, cause category, "
            "incident or system type, ignition/fire indicator, and release/leak "
            "field where available.",
            "",
            "The summary includes incident counts, summed estimated cost, summed "
            "fatalities, summed injuries, and a short dashboard risk note.",
            "",
            "This is a risk-awareness summary, not a formal integrity assessment.",
            "",
            "## Output Snapshot",
            "",
            f"- Grouped summary rows: {len(risk_summary):,}",
            "- Source incident rows used:",
            *source_count_lines,
            "",
            "## Limitations",
            "",
            "- PHMSA records are public US incident data, not PNG LNG operating "
            "data.",
            "- PHMSA incident forms and field definitions differ between LNG and "
            "Gas Transmission datasets.",
            "- Best-effort column matching is used where exact field names differ.",
            "- Cost, release, fire, injury, fatality, and cause fields depend on "
            "reported PHMSA form data and may change after supplemental reports.",
            "- The summary is intended for portfolio demonstration and dashboard "
            "screening, not regulatory analysis or a formal mechanical integrity "
            "assessment.",
            "",
        ]
    )


def print_profile(profile: dict) -> None:
    """Print the requested PHMSA profile details to the terminal."""
    dataset = profile["dataset"]
    data_file_names = ", ".join(path.name for path in profile["data_files"])
    dictionary_file_names = ", ".join(path.name for path in profile["dictionary_files"])
    if not dictionary_file_names:
        dictionary_file_names = "Not available"

    print()
    print(f"Dataset: {dataset['name']}")
    print(f"File names found: {data_file_names}")
    print(f"Data dictionary/description files found: {dictionary_file_names}")
    print(f"Main data file selected: {profile['main_data_file'].relative_to(PROJECT_ROOT)}")
    print(f"Row count: {profile['row_count']:,}")
    print("Column names:")
    print(", ".join(profile["columns"]))
    print()

    # The PHMSA Gas Transmission file has hundreds of columns. Printing every
    # column in five rows makes the terminal hard to read, so the console
    # preview focuses on the fields used for the dashboard summary. The full
    # all-column preview is preserved in the generated sample CSV.
    preview_columns = [
        column
        for column in profile["field_map"].values()
        if column is not None and column in profile["preview"].columns
    ]
    preview_columns = list(dict.fromkeys(preview_columns))
    preview = profile["preview"][preview_columns] if preview_columns else profile["preview"]

    print(
        f"First {PREVIEW_ROW_LIMIT} rows for mapped key fields "
        "(full rows are in the sample CSV):"
    )
    print(dataframe_to_text(preview))
    print()
    print("Missing value summary for key fields:")
    print(dataframe_to_text(profile["missing_summary"]))


def main() -> None:
    """Run the full PHMSA profiling and summary workflow."""
    print("Inspecting public PHMSA incident datasets...")
    print(f"Project root: {PROJECT_ROOT}")

    profiles = [profile_dataset(dataset) for dataset in DATASETS]

    normalized_frames = [
        normalize_dataset_for_summary(
            profile["dataset"]["name"], profile["dataframe"], profile["field_map"]
        )
        for profile in profiles
    ]
    normalized_incidents = pd.concat(normalized_frames, ignore_index=True)
    risk_summary = build_risk_summary(normalized_incidents)

    PROCESSED_OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    PROFILE_REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)

    risk_summary.to_csv(PROCESSED_OUTPUT_PATH, index=False)
    PROFILE_REPORT_PATH.write_text(build_profile_report(profiles), encoding="utf-8")
    RISK_REPORT_PATH.write_text(
        build_risk_report(profiles, risk_summary, normalized_incidents),
        encoding="utf-8",
    )

    for profile in profiles:
        print_profile(profile)

    print()
    print("PHMSA incident profiling complete.")
    print(f"Profile report written: {PROFILE_REPORT_PATH.relative_to(PROJECT_ROOT)}")
    print(f"Risk summary report written: {RISK_REPORT_PATH.relative_to(PROJECT_ROOT)}")
    print(f"Processed summary written: {PROCESSED_OUTPUT_PATH.relative_to(PROJECT_ROOT)}")
    for profile in profiles:
        sample_path = profile["dataset"]["sample_path"]
        print(
            f"Sample written: {sample_path.relative_to(PROJECT_ROOT)} "
            f"({profile['sample_rows']} rows)"
        )
    print(f"Risk summary rows created: {len(risk_summary):,}")


if __name__ == "__main__":
    main()
