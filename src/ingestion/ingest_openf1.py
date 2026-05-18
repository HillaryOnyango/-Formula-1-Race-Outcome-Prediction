import argparse
from pathlib import Path

import pandas as pd
import requests

from src.utils.io_utils import ensure_dir, save_dataframe

BASE_URL = "https://api.openf1.org/v1"


def fetch_endpoint(endpoint: str, params: dict) -> pd.DataFrame:
    response = requests.get(f"{BASE_URL}/{endpoint}", params=params, timeout=30)
    response.raise_for_status()
    return pd.DataFrame(response.json())


def main(year: int) -> None:
    output_dir = ensure_dir(Path("data/raw/openf1"))
    sessions = fetch_endpoint("sessions", {"year": year})
    save_dataframe(sessions, output_dir / f"sessions_{year}.csv")
    print(f"Saved {len(sessions):,} OpenF1 session rows.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--year", type=int, default=2026)
    args = parser.parse_args()
    main(args.year)
