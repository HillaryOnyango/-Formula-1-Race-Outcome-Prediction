from pathlib import Path

import pandas as pd

from src.utils.io_utils import ensure_dir, save_dataframe


RAW_PATH = Path("data/raw/ergast_results.csv")
OUTPUT_PATH = Path("data/processed/clean_results.parquet")


def main() -> None:
    ensure_dir("data/processed")

    df = pd.read_csv(RAW_PATH)

    df = df.drop_duplicates(subset=["race_id", "driver_id"])

    numeric_cols = ["season", "round", "grid", "finish_position", "points"]
    for col in numeric_cols:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    df["finish_position"] = df["finish_position"].fillna(99).astype(int)
    df["grid"] = df["grid"].fillna(0).astype(int)
    df["points"] = df["points"].fillna(0.0)

    text_cols = [
        "race_id",
        "race_name",
        "circuit_id",
        "driver_id",
        "driver_code",
        "given_name",
        "family_name",
        "constructor_id",
        "constructor_name",
        "status",
    ]

    for col in text_cols:
        if col in df.columns:
            df[col] = df[col].fillna("Unknown")

    save_dataframe(df, OUTPUT_PATH)

    print(f"Saved cleaned results to {OUTPUT_PATH} with {len(df)} rows.")
    print(df['finish_position'].value_counts().sort_index())


if __name__ == "__main__":
    main()
