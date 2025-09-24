"""
Data Wrangling Project: NYC Motor Vehicle Collisions
----------------------------------------------------
This script follows a step-by-step data-wrangling workflow for the
NYC Open Data "Motor Vehicle Collisions - Crashes" dataset.

Tasks covered (per project brief):
  1) Inspect the data
  2) Handle missing values
  3) Correct data types
  4) Clean text/categorical data
  5) Filter and group data
  6) Statistical summaries
  7) Export raw and cleaned data (JSON + Parquet)

Usage:
  python nyc_collisions_wrangling.py \
    --input_csv "Motor_Vehicle_Collisions_-_Crashes.csv" \
    --outdir "outputs"

Notes:
  - Parquet export requires 'pyarrow' or 'fastparquet'. If unavailable,
    the script will skip Parquet with a warning.
  - The script prints compact textual summaries to stdout and also saves
    key tables to CSV in the output directory for convenience.
"""

import argparse
import sys
from pathlib import Path
from typing import List
import numpy as np
import pandas as pd


# -------------------------------
# Configuration / Column schema
# -------------------------------
INJURY_COLS: List[str] = [
    "NUMBER OF PERSONS INJURED",
    "NUMBER OF PERSONS KILLED",
    "NUMBER OF PEDESTRIANS INJURED",
    "NUMBER OF PEDESTRIANS KILLED",
    "NUMBER OF CYCLIST INJURED",
    "NUMBER OF CYCLIST KILLED",
    "NUMBER OF MOTORIST INJURED",
    "NUMBER OF MOTORIST KILLED",
]

TEXT_COLS: List[str] = [
    "BOROUGH",
    "CONTRIBUTING FACTOR VEHICLE 1",
    "CONTRIBUTING FACTOR VEHICLE 2",
    "CONTRIBUTING FACTOR VEHICLE 3",
    "CONTRIBUTING FACTOR VEHICLE 4",
    "CONTRIBUTING FACTOR VEHICLE 5",
    "ON STREET NAME",
    "CROSS STREET NAME",
    "OFF STREET NAME",
]

DATE_COLS: List[str] = ["CRASH_DATE"]
TIME_COLS: List[str] = ["CRASH_TIME"]

LOCATION_COLS: List[str] = ["LATITUDE", "LONGITUDE"]

UNIQUE_KEY_COL = "UNIQUE KEY"


# -------------------------------
# Helper functions
# -------------------------------
def safe_to_parquet(df: pd.DataFrame, path: Path) -> None:
    try:
        df.to_parquet(path)
        print(f"[OK] Parquet written -> {path}")
    except Exception as e:
        print(f"[WARN] Skipping Parquet ({path.name}): {e}")


def ensure_columns_exist(df: pd.DataFrame, cols: List[str]) -> List[str]:
    """Return only columns that actually exist in the DataFrame."""
    return [c for c in cols if c in df.columns]


def load_raw(csv_path: Path) -> pd.DataFrame:
    print(f"[INFO] Loading CSV: {csv_path}")
    # Allow large file handling; low_memory=False to avoid mixed dtypes warnings
    df = pd.read_csv(csv_path, low_memory=False)
    print(f"[INFO] Shape: {df.shape}")
    print(f"[INFO] Columns ({len(df.columns)}): {list(df.columns)}\n")
    print("[HEAD]")
    print(df.head(3))
    print("\n[INFO()]")
    print(df.info())
    return df


def handle_missing_values(df: pd.DataFrame) -> pd.DataFrame:
    print("\n[STEP 2] Handle Missing Values")
    print(df.isnull().sum().sort_values(ascending=False).head(15))

    # Drop rows missing critical location info
    loc_cols = ensure_columns_exist(df, LOCATION_COLS)
    if loc_cols:
        before = df.shape[0]
        df = df.dropna(subset=loc_cols)
        after = df.shape[0]
        print(f"[INFO] Dropped rows missing {loc_cols}: {before - after} rows removed")

    # Fill injury/death counts with 0 where missing
    injuries = ensure_columns_exist(df, INJURY_COLS)
    if injuries:
        df[injuries] = df[injuries].fillna(0)

    # Fill contributing factor blanks with 'Unknown' (for VEHICLE 1 at least)
    if "CONTRIBUTING FACTOR VEHICLE 1" in df.columns:
        df["CONTRIBUTING FACTOR VEHICLE 1"] = (
            df["CONTRIBUTING FACTOR VEHICLE 1"].fillna("Unknown")
        )

    return df


def correct_types(df: pd.DataFrame) -> pd.DataFrame:
    print("\n[STEP 3] Correct Data Types")
    # Parse date/time
    for c in ensure_columns_exist(df, DATE_COLS):
        df[c] = pd.to_datetime(df[c], errors="coerce")
    for c in ensure_columns_exist(df, TIME_COLS):
        # Keep as string HH:MM or convert to timedelta; we keep as string parsed to time
        parsed = pd.to_datetime(df[c], format="%H:%M", errors="coerce")
        df[c] = parsed.dt.time

    # Convert injuries to Int64 (nullable integer)
    for c in ensure_columns_exist(df, INJURY_COLS):
        df[c] = pd.to_numeric(df[c], errors="coerce").astype("Int64")

    # Borough as category
    if "BOROUGH" in df.columns:
        df["BOROUGH"] = df["BOROUGH"].astype("category")

    print(df.dtypes)
    return df


def clean_text(df: pd.DataFrame) -> pd.DataFrame:
    print("\n[STEP 4] Clean Text/Categorical Data")
    for c in ensure_columns_exist(df, TEXT_COLS):
        if pd.api.types.is_string_dtype(df[c]) or df[c].dtype.name == "category":
            df[c] = df[c].astype("string").str.strip()

    # Standardize borough casing
    if "BOROUGH" in df.columns:
        df["BOROUGH"] = df["BOROUGH"].str.title()

    # Replace exact "Unspecified" with NaN (then can optionally backfill with 'Unknown')
    for c in ensure_columns_exist(df, [
        "CONTRIBUTING FACTOR VEHICLE 1",
        "CONTRIBUTING FACTOR VEHICLE 2",
        "CONTRIBUTING FACTOR VEHICLE 3",
        "CONTRIBUTING FACTOR VEHICLE 4",
        "CONTRIBUTING FACTOR VEHICLE 5",
    ]):
        df[c] = df[c].replace("Unspecified", pd.NA)

    return df


def filter_and_group(df: pd.DataFrame, outdir: Path) -> None:
    print("\n[STEP 5] Filter & Group Data")

    # Filter example: Manhattan subset
    if "BOROUGH" in df.columns:
        manhattan = df[df["BOROUGH"] == "Manhattan"]
        print(f"[INFO] Manhattan collisions: {manhattan.shape[0]}")

    # Year column
    if "CRASH_DATE" in df.columns:
        df["YEAR"] = df["CRASH_DATE"].dt.year

    # Group by borough: total collisions
    if "BOROUGH" in df.columns:
        borough_counts = df.groupby("BOROUGH").size().sort_values(ascending=False)
        print("\n[GROUP] Collisions by BOROUGH:")
        print(borough_counts)
        borough_counts.to_csv(outdir / "collisions_by_borough.csv", header=["count"])

    # Group by year: trend
    if "YEAR" in df.columns:
        yearly_counts = df.groupby("YEAR").size()
        print("\n[GROUP] Collisions by YEAR:")
        print(yearly_counts)
        yearly_counts.to_csv(outdir / "collisions_by_year.csv", header=["count"])

    # Pivot: collisions per borough per year
    if ("YEAR" in df.columns) and ("BOROUGH" in df.columns) and (UNIQUE_KEY_COL in df.columns):
        pivot = df.pivot_table(
            index="YEAR", columns="BOROUGH", values=UNIQUE_KEY_COL, aggfunc="count"
        )
        print("\n[PIVOT] Collisions per YEAR x BOROUGH (counts of UNIQUE KEY)")
        print(pivot.head())
        pivot.to_csv(outdir / "pivot_year_borough.csv")

    # Correlation matrix of injury columns
    injuries = ensure_columns_exist(df, INJURY_COLS)
    if injuries:
        corr = df[injuries].corr()
        print("\n[CORR] Injury columns correlation matrix")
        print(corr)
        corr.to_csv(outdir / "injury_correlation.csv")


def statistical_summaries(df: pd.DataFrame, outdir: Path) -> None:
    print("\n[STEP 6] Statistical Summaries")
    injuries = ensure_columns_exist(df, INJURY_COLS)
    if injuries:
        stats = df[injuries].describe()
        print("\n[DESCRIBE] Injury/Death Counts")
        print(stats)
        stats.to_csv(outdir / "injury_describe.csv")

        avg_injuries = df["NUMBER OF PERSONS INJURED"].mean()
        print(f"\n[STAT] Average injuries per collision: {avg_injuries:.4f}")

    # Top contributing factors
    if "CONTRIBUTING FACTOR VEHICLE 1" in df.columns:
        top_factors = df["CONTRIBUTING FACTOR VEHICLE 1"].value_counts(dropna=False).head(20)
        print("\n[TOP] Contributing Factor Vehicle 1 (Top 20)")
        print(top_factors)
        top_factors.to_csv(outdir / "top_contributing_factors_v1.csv", header=["count"])

    # Borough with most crashes
    if "BOROUGH" in df.columns:
        borough_counts = df.groupby("BOROUGH").size()
        if not borough_counts.empty:
            most_crashes = borough_counts.idxmax()
            print(f"\n[STAT] Borough with most crashes: {most_crashes}")
            borough_counts.to_csv(outdir / "collisions_by_borough_full.csv", header=["count"])


def export_raw_and_clean(csv_input: Path, df_clean: pd.DataFrame, outdir: Path) -> None:
    print("\n[STEP 7] Export Raw & Cleaned Data (JSON + Parquet)")
    raw_out_json = outdir / "collisions_raw.json"
    raw_out_parq = outdir / "collisions_raw.parquet"
    clean_out_json = outdir / "collisions_clean.json"
    clean_out_parq = outdir / "collisions_clean.parquet"

    # Raw
    print(f"[INFO] Reload raw for exact export: {csv_input}")
    df_raw = pd.read_csv(csv_input, low_memory=False)
    df_raw.to_json(raw_out_json, orient="records", lines=True)
    print(f"[OK] JSON written -> {raw_out_json}")
    safe_to_parquet(df_raw, raw_out_parq)

    # Cleaned
    df_clean.to_json(clean_out_json, orient="records", lines=True)
    print(f"[OK] JSON written -> {clean_out_json}")
    safe_to_parquet(df_clean, clean_out_parq)


def main(args=None):
    parser = argparse.ArgumentParser(description="NYC Motor Vehicle Collisions Data Wrangling")
    parser.add_argument("--input_csv", type=Path, required=True,
                        help="Path to 'Motor_Vehicle_Collisions_-_Crashes.csv'")
    parser.add_argument("--outdir", type=Path, default=Path("outputs"),
                        help="Directory to write outputs (tables + exports)")
    parsed = parser.parse_args(args=args)

    input_csv: Path = parsed.input_csv
    outdir: Path = parsed.outdir
    outdir.mkdir(parents=True, exist_ok=True)

    # 1) Inspect & load
    df = load_raw(input_csv)

    # Save a tiny sample for quick inspection (optional)
    sample_path = outdir / "sample_head.csv"
    df.head(50).to_csv(sample_path, index=False)
    print(f"[OK] Saved sample -> {sample_path}")

    # 2) Missing values
    df = handle_missing_values(df)

    # 3) Types
    df = correct_types(df)

    # 4) Clean text
    df = clean_text(df)

    # 5) Filter & group (and save tables)
    filter_and_group(df, outdir)

    # 6) Stats
    statistical_summaries(df, outdir)

    # 7) Export raw + cleaned
    export_raw_and_clean(input_csv, df, outdir)

    print("\n[DONE] Data wrangling workflow completed successfully.")


if __name__ == "__main__":
    sys.exit(main())
