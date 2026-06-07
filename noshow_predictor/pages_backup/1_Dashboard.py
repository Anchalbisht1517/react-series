"""Streamlit page: 1_Dashboard

Loads the processed dataset and displays high-level statistics plus EDA charts.
"""

import os
import sys
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Ensure src is discoverable
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
src_path = os.path.join(project_root, "src")
if src_path not in sys.path:
    sys.path.insert(0, src_path)

from noshow.config import project_config
from noshow.visualization.eda_charts import (
    plot_class_distribution,
    plot_sms_received_distribution,
    plot_wait_bucket_no_show,
    plot_no_show_by_weekday,
    plot_no_show_by_age_group,
    plot_correlation_heatmap,
)

st.set_page_config(page_title="Dashboard", page_icon="📊")

st.title("📊 Dashboard")

# ------------------------------------------------------------------
# Load data
# ------------------------------------------------------------------
processed_path = os.path.join(
    project_config.ROOT_DIR,
    project_config.config.get("data", {}).get(
        "processed_path", "data/processed/cleaned_appointments_v3.csv"
    )
)

if not os.path.exists(processed_path):
    st.error(f"Processed dataset not found at `{processed_path}`. Run the data pipeline first.")
    st.stop()

df = pd.read_csv(processed_path)

# ------------------------------------------------------------------
# KPIs
# ------------------------------------------------------------------
st.subheader("Key Metrics")

total_records = len(df)
no_show_rate = df["NoShow"].mean() if "NoShow" in df.columns else 0.0
high_risk_count = int((df["NoShow"] == 1).sum()) if "NoShow" in df.columns else 0

col1, col2, col3 = st.columns(3)
col1.metric("Total Records", f"{total_records:,}")
col2.metric("No-Show Rate", f"{no_show_rate:.2%}")
col3.metric("No-Show Count", f"{high_risk_count:,}")

st.markdown("---")

# ------------------------------------------------------------------
# Data preview
# ------------------------------------------------------------------
st.subheader("Processed Data Sample")
st.dataframe(df.head(10))

# ------------------------------------------------------------------
# Charts
# ------------------------------------------------------------------
st.subheader("Exploratory Charts")

chart_funcs = [
    ("Class Distribution", plot_class_distribution),
    ("SMS Received Distribution", plot_sms_received_distribution),
    ("No-Show by Wait Bucket", plot_wait_bucket_no_show),
    ("No-Show by Weekday", plot_no_show_by_weekday),
    ("No-Show by Age Group", plot_no_show_by_age_group),
    ("Correlation Heatmap", plot_correlation_heatmap),
]

for title, func in chart_funcs:
    try:
        fig = func(df, save=False)
        if fig is not None:
            st.pyplot(fig)
        else:
            # Some functions close the figure; re-render from file if saved
            pass
    except Exception as e:
        st.warning(f"Could not render '{title}': {e}")
