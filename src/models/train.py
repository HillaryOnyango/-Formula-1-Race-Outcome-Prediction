import argparse
from pathlib import Path

import joblib
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, precision_score, recall_score
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

from src.utils.io_utils import ensure_dir, read_dataframe

INPUT = Path("data/processed/model_table.parquet")
ARTIFACT_DIR = Path("artifacts")

NUMERIC_FEATURES = [
    "grid",
    "avg_finish_last_5",
    "driver_consistency_last_5",
    "team_points_last_5",
    "driver_points_last_5",
]
CATEGORICAL_FEATURES = ["driver_id", "constructor_id"]


def get_model(model_name: str):
    if model_name == "logistic_regression":
        return LogisticRegression(max_iter=1000, class_weight="balanced")
    if model_name == "random_forest":
        return RandomForestClassifier(n_estimators=300, random_state=42, class_weight="balanced")
    raise ValueError("model must be either logistic_regression or random_forest")


def train(target: str, model_name: str) -> None:
    df = read_dataframe(INPUT).sort_values(["season", "round"])
    test_season = df["season"].max()
    train_df = df[df["season"] < test_season]
    test_df = df[df["season"] == test_season]

    x_train = train_df[NUMERIC_FEATURES + CATEGORICAL_FEATURES]
    y_train = train_df[target]
    x_test = test_df[NUMERIC_FEATURES + CATEGORICAL_FEATURES]
    y_test = test_df[target]

    preprocessor = ColumnTransformer(
        transformers=[
            ("num", StandardScaler(), NUMERIC_FEATURES),
            ("cat", OneHotEncoder(handle_unknown="ignore"), CATEGORICAL_FEATURES),
        ]
    )
    pipeline = Pipeline(
        steps=[
            ("preprocessor", preprocessor),
            ("model", get_model(model_name)),
        ]
    )
    pipeline.fit(x_train, y_train)
    predictions = pipeline.predict(x_test)

    print({
        "target": target,
        "model": model_name,
        "test_season": int(test_season),
        "accuracy": round(accuracy_score(y_test, predictions), 4),
        "precision": round(precision_score(y_test, predictions, zero_division=0), 4),
        "recall": round(recall_score(y_test, predictions, zero_division=0), 4),
    })

    ensure_dir(ARTIFACT_DIR)
    joblib.dump(pipeline, ARTIFACT_DIR / f"{model_name}_{target}.joblib")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--target", default="is_top3", choices=["is_top3", "is_winner"])
    parser.add_argument("--model", default="random_forest", choices=["logistic_regression", "random_forest"])
    args = parser.parse_args()
    train(args.target, args.model)
