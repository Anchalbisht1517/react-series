# 🏥 Patient No-Show Risk Predictor

A machine learning web app that predicts whether a patient will show up for their medical appointment.

## Project Overview
- **Algorithm:** XGBoost Classifier
- **Dataset:** 110,527 patient records (Kaggle)
- **No-Show Detection Rate:** 83% Recall
- **Top Predictors:** Age, Days Waiting, SMS Received

## Features
- Patient no-show risk prediction
- Explainable AI using SHAP
- EDA Dashboard
- Streamlit Web App

## How to Run
pip install -r requirements.txt
streamlit run app.py