from pathlib import Path

import pandas as pd
from sqlalchemy import create_engine


INPUT_PATH = Path("data/processed/clean_results.parquet")

DB_URL = "postgresql+psycopg2://postgres@localhost:5432/formula1_db"


def main() -> None:
    df = pd.read_parquet(INPUT_PATH)

    engine = create_engine(DB_URL)

    drivers = (
        df[["driver_id", "driver_code", "given_name", "family_name"]]
        .drop_duplicates("driver_id")
        .rename(columns={"driver_code": "code"})
    )
    drivers["nationality"] = "Unknown"

    constructors = (
        df[["constructor_id", "constructor_name"]]
        .drop_duplicates("constructor_id")
        .rename(columns={"constructor_name": "name"})
    )
    constructors["nationality"] = "Unknown"

    races = (
        df[["race_id", "season", "round", "race_name", "circuit_id", "race_date"]]
        .drop_duplicates("race_id")
    )

    results = df[
        [
            "race_id",
            "driver_id",
            "constructor_id",
            "grid",
            "finish_position",
            "points",
            "status",
        ]
    ].drop_duplicates(["race_id", "driver_id"])

    with engine.begin() as conn:
        drivers.to_sql("drivers", conn, if_exists="append", index=False)
        constructors.to_sql("constructors", conn, if_exists="append", index=False)
        races.to_sql("races", conn, if_exists="append", index=False)
        results.to_sql("results", conn, if_exists="append", index=False)

    print("Loaded data into PostgreSQL successfully.")
    print(f"Drivers: {len(drivers)}")
    print(f"Constructors: {len(constructors)}")
    print(f"Races: {len(races)}")
    print(f"Results: {len(results)}")


if __name__ == "__main__":
    main()
