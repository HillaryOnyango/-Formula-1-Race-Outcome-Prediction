import argparse
import os
from pathlib import Path

import fastf1
import pandas as pd
from dotenv import load_dotenv

from src.utils.io_utils import ensure_dir, save_dataframe


def main(year: int, session: str) -> None:
    load_dotenv()
    cache_dir = os.getenv("FASTF1_CACHE_DIR", ".fastf1_cache")
    fastf1.Cache.enable_cache(cache_dir)

    output_dir = ensure_dir(Path("data/raw/fastf1"))
    schedule = fastf1.get_event_schedule(year)
    save_dataframe(schedule, output_dir / f"schedule_{year}.csv")

    rows: list[pd.DataFrame] = []
    for _, event in schedule.iterrows():
        try:
            race = fastf1.get_session(year, int(event["RoundNumber"]), session)
            race.load(laps=True, telemetry=False, weather=True)
            laps = race.laps.copy()
            laps["season"] = year
            laps["round"] = int(event["RoundNumber"])
            rows.append(laps)
        except Exception as exc:  # keep ingestion resilient while developing
            print(f"Skipping round {event['RoundNumber']}: {exc}")

    if rows:
        lap_data = pd.concat(rows, ignore_index=True)
        save_dataframe(lap_data, output_dir / f"laps_{year}_{session}.csv")
        print(f"Saved {len(lap_data):,} FastF1 lap rows.")
    else:
        print("No FastF1 lap data saved.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--year", type=int, default=2025)
    parser.add_argument("--session", type=str, default="R")
    args = parser.parse_args()
    main(args.year, args.session)
