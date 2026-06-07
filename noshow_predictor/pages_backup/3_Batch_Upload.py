"""Streamlit page: 3_Batch_Upload

Accepts a user-uploaded CSV, runs the prediction pipeline on every row,
and allows the user to download the results.
"""

import os
import sys
import streamlit as st
import pandas as pd

# Ensure src is discoverable
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
src_path = os.path.join(project_root, "src")
if src_path not in sys.path:
    sys.path.insert(0, src_path)

from noshow.pipeline.prediction_pipeline import PredictionPipeline
from noshow.exception import NoShowException

st.set_page_config(page_title="Batch Upload", page_icon="📁")

st.title("📁 Batch Upload")

st.markdown("""
Upload a CSV file containing patient data. The prediction pipeline will score
every row and output risk probabilities and tiers.

**Expected columns** (matching the processed dataset before one-hot encoding):
- `Age`, `Gender`, `Scholarship`, `Hypertension`, `Diabetes`, `Alcoholism`, `Handicap`, `SMS_received`
- `days_waiting`, `appointment_weekday`, `previous_no_shows`, `Neighbourhood`
""")

uploaded_file = st.file_uploader("Choose a CSV file", type="csv")

if uploaded_file is not None:
    try:
        input_df = pd.read_csv(uploaded_file)
        st.subheader("Uploaded Data Preview")
        st.dataframe(input_df.head())

        with st.spinner("Running batch predictions..."):
            pipeline = PredictionPipeline()
            results_df = pipeline.predict_batch(input_df)

        st.subheader("Prediction Results")
        st.dataframe(results_df)

        # Download button
        csv = results_df.to_csv(index=False).encode("utf-8")
        st.download_button(
            label="Download Results as CSV",
            data=csv,
            file_name="batch_predictions.csv",
            mime="text/csv",
        )

        # Summary stats
        st.subheader("Summary")
        tier_counts = results_df["risk_tier"].value_counts()
        c1, c2, c3 = st.columns(3)
        c1.metric("High Risk", f"{tier_counts.get('High', 0)}")
        c2.metric("Medium Risk", f"{tier_counts.get('Medium', 0)}")
        c3.metric("Low Risk", f"{tier_counts.get('Low', 0)}")

    except NoShowException as e:
        st.error(f"Pipeline error: {e}")
        st.info("Make sure the model artifacts (preprocessor + xgboost) exist.")
    except Exception as e:
        st.error(f"Unexpected error: {e}")
