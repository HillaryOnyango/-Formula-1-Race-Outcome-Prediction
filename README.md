# 🏎️ Formula 1 Race Outcome Prediction (2026 Season)

A production-grade Data Science + Data Engineering project that builds a complete pipeline for analyzing and predicting Formula 1 race outcomes.

This project integrates multiple APIs, engineers predictive features, trains machine learning models, and serves results through a Streamlit application — all managed using UV for fast, reproducible environments.

---

## 🚀 Project Overview

### Problem Statement
Formula 1 race outcomes are influenced by driver skill, constructor performance, qualifying position, track characteristics, and race dynamics.

Most projects stop at dashboards — this project delivers a full end-to-end pipeline:
Data ingestion → Processing → Feature Engineering → Modeling → Deployment

---

## 🎯 Objectives

- Build a multi-source F1 data platform (2021–2025 historical + 2026 updates)
- Engineer race-level and driver-level features
- Train models to predict:
  - Race winner
  - Top 3 finish
- Deploy predictions in an interactive app

---

## ⚡ Why UV?

This project uses UV instead of pip for:
- Faster dependency resolution
- Reproducible environments
- Lockfile-based dependency management
- Cleaner Python workflows

---

## 🧱 Architecture

Ergast API | OpenF1 API | FastF1  
        ↓  
   Ingestion Layer  
        ↓  
     Raw Data  
        ↓  
  Data Processing  
        ↓  
  Feature Engineering  
        ↓  
     Modeling  
        ↓  
   Artifacts  
        ↓  
   Streamlit App  

---

## 📂 Project Structure

formula1-race-prediction-project/
├── app/
├── artifacts/
├── config/
├── data/
├── notebooks/
├── sql/
├── src/
├── tests/
├── pyproject.toml
├── uv.lock
└── README.md

---

## ⚙️ Pipeline Overview

1. Data ingestion from APIs  
2. Data cleaning and validation  
3. Feature engineering  
4. Model training and evaluation  
5. Deployment via Streamlit  

---

## 🤖 Modeling

Targets:
- is_top3
- is_winner
- points (optional)

Models:
- Logistic Regression
- Random Forest / XGBoost

---

## 📊 Evaluation

- Accuracy
- Precision / Recall
- Confusion Matrix

---

## 📺 Deployment

Run:
uv run streamlit run app/streamlit_app.py

---

## ⚡ Quickstart

Install UV:
curl -Ls https://astral.sh/uv/install.sh | sh

Install dependencies:
uv sync

Run pipeline:
uv run python src/ingestion/ingest_ergast.py --start-season 2021 --end-season 2025
uv run python src/processing/clean_data.py
uv run python src/features/build_features.py
uv run python src/models/train.py --target is_top3

Launch app:
uv run streamlit run app/streamlit_app.py

---

## 📌 Portfolio Impact

This project demonstrates:
- Data engineering pipelines
- Machine learning workflows
- End-to-end deployment

---

## 👨‍💻 Author

Hillary Onyango Amolo
