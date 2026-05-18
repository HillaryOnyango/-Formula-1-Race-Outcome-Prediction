# Analyzing and Predicting Formula 1 Race Results – 2026 Season

A production-style **Data Science + Data Engineering** portfolio project for collecting Formula 1 data, building machine learning features, training prediction models, and deploying an interactive Streamlit app.

The project combines historical race data, live/session data, and model-ready feature engineering to predict:

- whether a driver finishes in the **Top 3**
- whether a driver **wins the race**
- optional: how many **points** a driver scores

---

## 1. Project Overview

Formula 1 race outcomes are influenced by driver skill, constructor strength, qualifying position, track characteristics, reliability, weather, and strategy. This project is designed to go beyond a simple notebook by building a full end-to-end analytics workflow.

### Objectives

- Collect F1 data from multiple APIs.
- Store raw and processed data in a clean project structure.
- Build a driver-race modeling table.
- Engineer predictive features such as recent form, qualifying impact, team strength, and track history.
- Train baseline and advanced ML models.
- Evaluate model performance using classification metrics.
- Deploy predictions and visual insights in Streamlit.

---

## 2. Data Sources

| Source | Purpose |
|---|---|
| Ergast API | Historical schedules, results, qualifying, drivers, constructors, and lap data |
| OpenF1 API | Live/session data, laps, telemetry-style race-week updates |
| FastF1 | Python interface for structured session timing, weather, and lap-level data |

### Integration Strategy

The project uses common keys across sources:

- `season`
- `round`
- `race_id`
- `driver_id` or `driver_number`
- `constructor_id`
- `session_type`
- UTC timestamps

---

## 3. Architecture

```text
Ergast API        OpenF1 API        FastF1
    │                 │               │
    └────────────┬────┴────┬──────────┘
                 │
        src/ingestion/*.py
                 │
                 ▼
          data/raw/*.csv
                 │
                 ▼
   src/processing/clean_data.py
                 │
                 ▼
 data/processed/clean_results.parquet
                 │
                 ▼
   src/features/build_features.py
                 │
                 ▼
 data/processed/model_table.parquet
                 │
                 ▼
 src/models/train.py + evaluate.py
                 │
                 ▼
 artifacts/*.joblib + metrics/*.json
                 │
                 ▼
        app/streamlit_app.py
```

---

## 4. Project Structure

```text
formula1-race-prediction-project/
├── app/
│   └── streamlit_app.py
├── artifacts/
│   └── .gitkeep
├── config/
│   └── settings.yaml
├── data/
│   ├── raw/
│   │   └── .gitkeep
│   └── processed/
│       └── .gitkeep
├── notebooks/
│   └── 01_eda.ipynb
├── sql/
│   └── schema_postgres.sql
├── src/
│   ├── ingestion/
│   │   ├── ingest_ergast.py
│   │   ├── ingest_openf1.py
│   │   └── ingest_fastf1.py
│   ├── processing/
│   │   └── clean_data.py
│   ├── features/
│   │   └── build_features.py
│   ├── models/
│   │   ├── train.py
│   │   └── evaluate.py
│   └── utils/
│       ├── db.py
│       └── io_utils.py
├── tests/
│   └── test_features.py
├── .env.example
├── .gitignore
├── requirements.txt
└── README.md
```

---

## 5. Setup

### Create and activate a virtual environment

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### Install dependencies

```bash
pip install -r requirements.txt
```

### Configure environment variables

```bash
cp .env.example .env
```

Update `.env` if you plan to use PostgreSQL.

---

## 6. How to Run the Pipeline

### 1. Ingest data

```bash
python src/ingestion/ingest_ergast.py --start-season 2021 --end-season 2025
python src/ingestion/ingest_openf1.py --year 2026
python src/ingestion/ingest_fastf1.py --year 2025 --session R
```

### 2. Clean data

```bash
python src/processing/clean_data.py
```

### 3. Build features

```bash
python src/features/build_features.py
```

### 4. Train a model

```bash
python src/models/train.py --target is_top3 --model random_forest
```

### 5. Evaluate a model

```bash
python src/models/evaluate.py --target is_top3
```

### 6. Launch the app

```bash
streamlit run app/streamlit_app.py
```

---

## 7. Modeling Approach

### Main prediction targets

| Target | Type | Description |
|---|---|---|
| `is_top3` | Classification | 1 if the driver finishes on the podium |
| `is_winner` | Classification | 1 if the driver wins the race |
| `points` | Regression | Number of championship points scored |

### Required models

- Logistic Regression baseline
- Random Forest classifier
- Optional XGBoost classifier

### Evaluation metrics

- Accuracy
- Precision
- Recall
- Confusion matrix

For podium prediction, recall is especially important because it shows how many real podium finishers the model captured.

---

## 8. Key Features

Planned feature groups:

- average finishing position
- qualifying position
- recent form over last 3–5 races
- constructor rolling points
- driver consistency score
- track-specific driver performance
- median race pace
- DNF/reliability trend

---

## 9. Database Design

Core PostgreSQL tables:

- `drivers`
- `constructors`
- `races`
- `results`
- `lap_times`
- `telemetry`

See [`sql/schema_postgres.sql`](sql/schema_postgres.sql).

---

## 10. Portfolio Deliverables

- Clean GitHub repository
- Modular ingestion scripts
- Reproducible data pipeline
- PostgreSQL schema
- Processed modeling dataset
- EDA notebook
- Feature engineering pipeline
- Trained model artifacts
- Evaluation report
- Streamlit prediction app

---

## 11. Roadmap

- [ ] Complete Ergast ingestion
- [ ] Add OpenF1 session ingestion
- [ ] Add FastF1 lap/weather extraction
- [ ] Build cleaned model table
- [ ] Add feature engineering logic
- [ ] Train baseline model
- [ ] Add Random Forest/XGBoost model
- [ ] Build Streamlit dashboard
- [ ] Add tests and CI workflow

---

## 12. License

This project is intended for learning and portfolio use.
