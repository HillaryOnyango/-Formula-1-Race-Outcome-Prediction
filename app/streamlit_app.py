from pathlib import Path

import joblib
import pandas as pd
import streamlit as st

MODEL_PATH = Path("artifacts/random_forest_is_top3.joblib")
DATA_PATH = Path("data/processed/model_table.parquet")
FEATURES = [
    "grid",
    "avg_finish_last_5",
    "driver_consistency_last_5",
    "team_points_last_5",
    "driver_points_last_5",
    "driver_id",
    "constructor_id",
]

st.set_page_config(page_title="F1 Race Prediction", layout="wide")
st.title("Formula 1 Race Outcome Prediction")
st.write("Explore driver form and generate podium probability predictions.")

if not DATA_PATH.exists():
    st.warning("Model table not found. Run the ingestion, cleaning, and feature scripts first.")
    st.stop()

df = pd.read_parquet(DATA_PATH)

st.subheader("Dataset Preview")
st.dataframe(df.head(50), use_container_width=True)

col1, col2 = st.columns(2)
with col1:
    st.metric("Rows", f"{len(df):,}")
with col2:
    st.metric("Seasons", f"{df['season'].min()}–{df['season'].max()}")

st.subheader("Driver Form")
selected_driver = st.selectbox("Select driver", sorted(df["driver_id"].dropna().unique()))
driver_df = df[df["driver_id"] == selected_driver].sort_values(["season", "round"])
st.line_chart(driver_df.set_index("race_id")[["finish_position", "avg_finish_last_5"]])

st.subheader("Podium Prediction")
if not MODEL_PATH.exists():
    st.info("Train the default model first: python src/models/train.py --target is_top3 --model random_forest")
else:
    model = joblib.load(MODEL_PATH)
    latest_season = df["season"].max()
    race_options = df[df["season"] == latest_season]["race_name"].dropna().unique()
    selected_race = st.selectbox("Select race", sorted(race_options))
    race_df = df[(df["season"] == latest_season) & (df["race_name"] == selected_race)].copy()
    probabilities = model.predict_proba(race_df[FEATURES])[:, 1]
    race_df["podium_probability"] = probabilities
    output = race_df.sort_values("podium_probability", ascending=False)[
        ["driver_id", "constructor_id", "grid", "podium_probability"]
    ]
    st.dataframe(output, use_container_width=True)

# -----------------------------
# Podium Evaluation
# -----------------------------
st.header("Podium Evaluation")

st.write(
    "Compare the model's predicted podium against the actual race podium."
)

evaluation_race = st.selectbox(
    "Select race to evaluate",
    sorted(df["race_name"].dropna().unique()),
    key="evaluation_race",
)

eval_df = df[df["race_name"] == evaluation_race].copy()

if not eval_df.empty:
    eval_df["podium_probability"] = model.predict_proba(
        eval_df[NUMERIC_FEATURES + CATEGORICAL_FEATURES]
    )[:, 1]

    predicted_top3 = (
        eval_df.sort_values("podium_probability", ascending=False)
        .head(3)
        ["driver_id"]
        .tolist()
    )

    actual_top3 = (
        eval_df[eval_df["finish_position"] <= 3]
        .sort_values("finish_position")
        ["driver_id"]
        .tolist()
    )

    correct = len(set(predicted_top3).intersection(actual_top3))
    podium_accuracy = correct / 3

    col1, col2, col3 = st.columns(3)

    col1.metric("Correct Podium Picks", f"{correct}/3")
    col2.metric("Podium Accuracy", f"{podium_accuracy:.2%}")
    col3.metric("Race", evaluation_race)

    comparison_df = pd.DataFrame({
        "predicted_podium": predicted_top3,
        "actual_podium": actual_top3
    })

    st.subheader("Predicted vs Actual Podium")
    st.dataframe(comparison_df, use_container_width=True)
