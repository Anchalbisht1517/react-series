"""Streamlit page: 5_SHAP_Explainability

Renders saved SHAP plots and provides a brief explanation of what SHAP shows.
"""

import os
import sys
import streamlit as st

# Ensure src is discoverable
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
src_path = os.path.join(project_root, "src")
if src_path not in sys.path:
    sys.path.insert(0, src_path)

from noshow.visualization.shap_plots import get_shap_paths, render_image

st.set_page_config(page_title="SHAP Explainability", page_icon="🔍")

st.title("🔍 SHAP Explainability")

st.markdown("""
**What is SHAP?**

SHAP (SHapley Additive exPlanations) values explain how each feature pushes
the model's prediction away from the baseline (average) output.

- **Positive SHAP value** → the feature *increases* the predicted no-show probability.
- **Negative SHAP value** → the feature *decreases* the predicted no-show probability.
- **Magnitude** → how strongly the feature influences this specific prediction.

Use the plots below to understand **global** feature importance and **individual**
patient explanations.
""")

st.markdown("---")

# ------------------------------------------------------------------
# Load plot paths
# ------------------------------------------------------------------
paths = get_shap_paths()

# ------------------------------------------------------------------
# Summary bar
# ------------------------------------------------------------------
st.subheader("1. Global Feature Importance (Bar)")
if os.path.exists(paths["summary_bar"]):
    fig = render_image(paths["summary_bar"], title="SHAP Summary Bar")
    st.pyplot(fig)
else:
    st.info("Summary bar plot not found. Run the explainability pipeline first.")

st.markdown("""
*The bar chart ranks features by their average absolute SHAP value across the
dataset. Higher bars mean the feature has a larger overall impact on predictions.*
""")

st.markdown("---")

# ------------------------------------------------------------------
# Summary dot
# ------------------------------------------------------------------
st.subheader("2. Feature Impact Direction (Dot Plot)")
if os.path.exists(paths["summary_dot"]):
    fig = render_image(paths["summary_dot"], title="SHAP Summary Dot")
    st.pyplot(fig)
else:
    st.info("Summary dot plot not found. Run the explainability pipeline first.")

st.markdown("""
*Each dot is a single prediction. The horizontal position shows the SHAP value
(direction + magnitude), and the color shows the actual feature value
(red = high, blue = low).*
""")

st.markdown("---")

# ------------------------------------------------------------------
# Waterfall
# ------------------------------------------------------------------
st.subheader("3. Individual Patient Explanation (Waterfall)")
if os.path.exists(paths["waterfall"]):
    fig = render_image(paths["waterfall"], title="SHAP Waterfall")
    st.pyplot(fig)
else:
    st.info("Waterfall plot not found. Run the explainability pipeline first.")

st.markdown("""
*The waterfall plot breaks down one specific prediction. Starting from the
base value (average model output), each bar shows how a feature pushes the
prediction up (red) or down (blue) to reach the final probability.*
""")
