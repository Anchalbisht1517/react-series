"""EDA Explorer page for CarePredict. Shows data distribution and exploratory charts."""

import streamlit as st
import os
import pandas as pd
from noshow.config import project_config
from noshow.visualization.eda_charts import (
    plot_class_distribution,
    plot_sms_received_distribution,
    plot_wait_bucket_no_show,
    plot_no_show_by_weekday,
    plot_no_show_by_age_group,
    plot_correlation_heatmap,
)

def render_eda_explorer():
    """Render the EDA Explorer page."""
    st.html("<h3 style='margin:0 0 10px 0; color:#0f1f3d; font-weight:600;'>EDA Explorer</h3>")
    st.html("<p style='color:#64748b; font-size:13px;'>Investigate historical appointments metadata, demographic splits, and statistical correlation heatmaps.</p>")
    
    # ------------------------------------------------------------------
    # Load dataset
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
    
    # Data summary card
    st.html(f"""
    <div class="card card-sky-blue" style="padding:15px; margin-bottom:20px;">
        <div style="display:flex; justify-content:space-between; align-items:center;">
            <div>
                <span style="font-size:13px; font-weight:600; color:#0f1f3d;">Dataset Summary</span>
                <div style="font-size:11px; color:#94a3b8; margin-top:2px;">Cleaned appointments roster loaded from disk</div>
            </div>
            <div style="text-align:right;">
                <span style="font-size:18px; font-weight:600; color:#0f1f3d;">{len(df):,}</span>
                <span style="font-size:11px; color:#64748b;">total rows</span>
            </div>
        </div>
    </div>
    """)
    
    # Tab filters for different analysis categories
    chart_tab = st.selectbox(
        "Select EDA Chart Section",
        [
            "Demographics & Scheduling Lead", 
            "SMS Reminders & Weekday Splits", 
            "Data Roster Samples & Correlations"
        ]
    )
    
    if chart_tab == "Demographics & Scheduling Lead":
        col1, col2 = st.columns(2)
        with col1:
            with st.container(border=True):
                st.html("<div class='card-title-text' style='margin-bottom:10px;'>No-Show Rate by Age Group</div>")
                fig = plot_no_show_by_age_group(df, save=False)
                if fig is not None:
                    st.pyplot(fig)
        with col2:
            with st.container(border=True):
                st.html("<div class='card-title-text' style='margin-bottom:10px;'>No-Show Rate by Scheduling Wait Bucket</div>")
                fig = plot_wait_bucket_no_show(df, save=False)
                if fig is not None:
                    st.pyplot(fig)
            
    elif chart_tab == "SMS Reminders & Weekday Splits":
        col1, col2 = st.columns(2)
        with col1:
            with st.container(border=True):
                st.html("<div class='card-title-text' style='margin-bottom:10px;'>SMS Reminder Count Splits</div>")
                fig = plot_sms_received_distribution(df, save=False)
                if fig is not None:
                    st.pyplot(fig)
        with col2:
            with st.container(border=True):
                st.html("<div class='card-title-text' style='margin-bottom:10px;'>No-Show Rate by Weekday</div>")
                fig = plot_no_show_by_weekday(df, save=False)
                if fig is not None:
                    st.pyplot(fig)
            
    elif chart_tab == "Data Roster Samples & Correlations":
        # Class distribution + heatmap
        col1, col2 = st.columns([2, 3])
        with col1:
            with st.container(border=True):
                st.html("<div class='card-title-text' style='margin-bottom:10px;'>No-Show Class Distribution</div>")
                fig = plot_class_distribution(df, save=False)
                if fig is not None:
                    st.pyplot(fig)
        with col2:
            with st.container(border=True):
                st.html("<div class='card-title-text' style='margin-bottom:10px;'>Pearson Correlation Heatmap</div>")
                fig = plot_correlation_heatmap(df, save=False)
                if fig is not None:
                    st.pyplot(fig)
            
        with st.expander("Show Processed Data Roster Head (10 records)"):
            st.dataframe(df.head(10), use_container_width=True)
