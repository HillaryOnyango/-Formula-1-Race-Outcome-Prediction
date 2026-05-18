import argparse
from pathlib import Path

import pandas as pd
import requests

from src.utils.io_utils import ensure_dir, save_dataframe

BASE_URL = "https://api.jolpi.ca/ergast/f1"


def fetch_url(url: str) -> dict:
    response = requests.get(url, timeout=30)
    response.raise_for_status()
    return response.json()


def fetch_race_results(season: int) -> pd.DataFrame:
    rows = []
    limit = 100
    offset = 0

    while True:
        url = f"{BASE_URL}/{season}/results.json?limit={limit}&offset={offset}"
        data = fetch_url(url)

        mrdata = data["MRData"]
        total = int(mrdata["total"])
        races = mrdata["RaceTable"]["Races"]

        for race in races:
            season_value = int(race["season"])
            round_value = int(race["round"])
            race_id = f"{season_value}_{round_value}"

            for result in race["Results"]:
                driver = result["Driver"]
                constructor = result["Constructor"]

                rows.append(
                    {
                        "race_id": race_id,
                        "season": season_value,
                        "round": round_value,
                        "race_name": race["raceName"],
                        "race_date": race.get("date"),
                        "circuit_id": race["Circuit"]["circuitId"],
                        "driver_id": driver["driverId"],
                        "driver_code": driver.get("code"),
                        "given_name": driver.get("givenName"),
                        "family_name": driver.get("familyName"),
                        "constructor_id": constructor["constructorId"],
                        "constructor_name": constructor["name"],
                        "grid": int(result.get("grid", 0)),
                        "finish_position": int(result.get("positionOrder", result.get("position", 0))),
                        "points": float(result.get("points", 0)),
                        "status": result.get("status"),
                    }
                )

        offset += limit

        if offset >= total:
            break

    return pd.DataFrame(rows)


def main(start_season: int, end_season: int) -> None:
    ensure_dir("data/raw")

    frames = [
        fetch_race_results(season)
        for season in range(start_season, end_season + 1)
    ]

    df = pd.concat(frames, ignore_index=True)

    output_path = Path("data/raw/ergast_results.csv")
    save_dataframe(df, output_path)

    print(f"Saved {len(df)} Ergast result rows to {output_path}")
    print(df["finish_position"].value_counts().sort_index().head(25))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--start-season", type=int, required=True)
    parser.add_argument("--end-season", type=int, required=True)
    args = parser.parse_args()

    main(args.start_season, args.end_season)
