"""Streamlit page: 4_Model_Performance

Displays the model comparison metrics table, confusion matrices, and ROC curves.
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

from noshow.visualization.evaluation_plots import (
    get_confusion_matrix_path,
    get_roc_curve_path,
    render_image,
)

st.set_page_config(page_title="Model Performance", page_icon="📈")

st.title("📈 Model Performance")

# ------------------------------------------------------------------
# Metrics table
# ------------------------------------------------------------------
comparison_path = os.path.join(project_root, "outputs", "model_comparison.csv")

if os.path.exists(comparison_path):
    comparison_df = pd.read_csv(comparison_path)
    st.subheader("Model Comparison")
    st.dataframe(comparison_df.style.highlight_max(subset=["recall", "roc_auc"], color="green"))
else:
    st.warning("`outputs/model_comparison.csv` not found. Run model evaluation first.")

st.markdown("---")

# ------------------------------------------------------------------
# Confusion matrices
# ------------------------------------------------------------------
st.subheader("Confusion Matrices")

models = ["LogisticRegression", "DecisionTree", "RandomForest", "XGBoost"]
cols = st.columns(2)
for idx, model_name in enumerate(models):
    path = get_confusion_matrix_path(model_name)
    with cols[idx % 2]:
        if os.path.exists(path):
            fig = render_image(path, title=model_name)
            st.pyplot(fig)
        else:
            st.info(f"Confusion matrix for {model_name} not yet generated.")

st.markdown("---")

# ------------------------------------------------------------------
# ROC curve
# ------------------------------------------------------------------
st.subheader("ROC Curves")
roc_path = get_roc_curve_path()
if os.path.exists(roc_path):
    fig = render_image(roc_path, title="ROC Curves")
    st.pyplot(fig)
else:
    st.info("ROC curve plot not yet generated.")
