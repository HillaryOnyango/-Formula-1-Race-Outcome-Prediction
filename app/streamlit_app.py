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
