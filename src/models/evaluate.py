import argparse
from pathlib import Path

import joblib
from sklearn.metrics import classification_report, confusion_matrix

from src.models.train import CATEGORICAL_FEATURES, NUMERIC_FEATURES
from src.utils.io_utils import read_dataframe

DATA_PATH = Path("data/processed/model_table.parquet")


def evaluate(target: str, model_name: str) -> None:
    model_path = Path("artifacts") / f"{model_name}_{target}.joblib"
    if not model_path.exists():
        raise FileNotFoundError(f"Model not found: {model_path}. Train it first.")

    df = read_dataframe(DATA_PATH).sort_values(["season", "round"])
    test_season = df["season"].max()
    test_df = df[df["season"] == test_season]

    model = joblib.load(model_path)
    x_test = test_df[NUMERIC_FEATURES + CATEGORICAL_FEATURES]
    y_test = test_df[target]
    predictions = model.predict(x_test)

    print("Classification report")
    print(classification_report(y_test, predictions, zero_division=0))
    print("Confusion matrix")
    print(confusion_matrix(y_test, predictions))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--target", default="is_top3", choices=["is_top3", "is_winner"])
    parser.add_argument("--model", default="random_forest", choices=["logistic_regression", "random_forest"])
    args = parser.parse_args()
    evaluate(args.target, args.model)
