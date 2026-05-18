from pathlib import Path
import pandas as pd

from src.utils.io_utils import ensure_dir, read_dataframe, save_dataframe

INPUT = Path("data/processed/clean_results.parquet")
OUTPUT = Path("data/processed/model_table.parquet")


def build_model_table(df: pd.DataFrame) -> pd.DataFrame:
    df = df.sort_values(["season", "round", "driver_id"]).copy()

    df["is_top3"] = (df["finish_position"] <= 3).astype(int)
    df["is_winner"] = (df["finish_position"] == 1).astype(int)

    df["avg_finish_last_5"] = df.groupby("driver_id")["finish_position"].transform(
        lambda s: s.shift(1).rolling(5, min_periods=1).mean()
    )

    df["driver_consistency_last_5"] = df.groupby("driver_id")["finish_position"].transform(
        lambda s: s.shift(1).rolling(5, min_periods=2).std()
    )

    df["team_points_last_5"] = df.groupby("constructor_id")["points"].transform(
        lambda s: s.shift(1).rolling(5, min_periods=1).mean()
    )

    df["driver_points_last_5"] = df.groupby("driver_id")["points"].transform(
        lambda s: s.shift(1).rolling(5, min_periods=1).mean()
    )

    df["grid"] = df["grid"].replace(0, df["grid"].median())

    selected_columns = [
        "season",
        "round",
        "race_id",
        "race_name",
        "driver_id",
        "constructor_id",
        "grid",
        "finish_position",
        "points",
        "avg_finish_last_5",
        "driver_consistency_last_5",
        "team_points_last_5",
        "driver_points_last_5",
        "is_top3",
        "is_winner",
    ]

    model_table = df[selected_columns].copy()

    numeric_cols = [
        "grid",
        "finish_position",
        "points",
        "avg_finish_last_5",
        "driver_consistency_last_5",
        "team_points_last_5",
        "driver_points_last_5",
    ]

    for col in numeric_cols:
        model_table[col] = model_table[col].fillna(model_table[col].median())

    return model_table


def main() -> None:
    ensure_dir("data/processed")
    df = read_dataframe(INPUT)
    model_table = build_model_table(df)
    save_dataframe(model_table, OUTPUT)

    print(f"Saved model table to {OUTPUT} with {len(model_table)} rows.")
    print(model_table.columns.tolist())


if __name__ == "__main__":
    main()
