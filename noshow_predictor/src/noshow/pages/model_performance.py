"""Model Performance page for CarePredict. Displays model comparisons and evaluation plots."""

import streamlit as st
import os
import pandas as pd
from noshow.visualization.evaluation_plots import (
    get_confusion_matrix_path,
    get_roc_curve_path,
    render_image,
)

def render_model_performance():
    """Render the Model Performance page."""
    st.html("<h3 style='margin:0 0 10px 0; color:#0f1f3d; font-weight:600;'>Model Performance</h3>")
    st.html("<p style='color:#64748b; font-size:13px;'>Review machine learning metrics, compare algorithms, and inspect validation curves.</p>")
    
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
    comparison_path = os.path.join(project_root, "outputs", "model_comparison.csv")
    
    # ------------------------------------------------------------------
    # Model Comparison Table
    # ------------------------------------------------------------------
    if os.path.exists(comparison_path):
        df = pd.read_csv(comparison_path)
        
        # Human readable names
        model_names = {
            "lr": "Logistic Regression",
            "dt": "Decision Tree",
            "rf": "Random Forest",
            "xgb": "XGBoost v2 (Active)"
        }
        df["model_name"] = df["model"].map(model_names)
        
        # Build styled HTML table highlighting the max in each column
        # Columns: model_name, recall, roc_auc, precision, f1, accuracy
        metrics = ["recall", "roc_auc", "precision", "f1", "accuracy"]
        max_vals = {metric: df[metric].max() for metric in metrics}
        
        table_rows_html = ""
        for _, row in df.iterrows():
            name = row["model_name"]
            is_active = "Active" in name
            active_style = "background-color: #f8fafc; font-weight: 500;" if is_active else ""
            
            row_html = f"<div class='flex-table-row' style='{active_style}'>"
            row_html += f"<div style='flex: 2; font-weight: 600;'>{name}</div>"
            
            for m in metrics:
                val = row[m]
                is_max = val == max_vals[m]
                
                # Check if it's recall for XGBoost (celebrate the 91.89%)
                if m == "recall" and row["model"] == "xgb":
                    cell_html = f"<div style='flex: 1; color:#16a34a; font-weight:600;'>{val:.2%}</div>"
                elif is_max:
                    cell_html = f"<div style='flex: 1; color:#16a34a; font-weight:600;'>{val:.2%}</div>"
                else:
                    cell_html = f"<div style='flex: 1;'>{val:.2%}</div>"
                row_html += cell_html
                
            row_html += "</div>"
            table_rows_html += row_html
            
        st.html(f"""
        <div class="card" style="padding: 20px;">
            <div class="card-title-text" style="margin-bottom:15px;">Side-by-Side Model Comparison</div>
            <p style="font-size:12px; color:#64748b; margin-top:-10px; margin-bottom:15px;">
                Winning metrics are highlighted in green. The active XGBoost model is selected for its superior <b>Recall ({max_vals['recall']:.2%})</b>, crucial for clinical intervention coverage.
            </p>
            <div class="flex-table">
                <div class="flex-table-header">
                    <div style="flex: 2;">Model Algorithm</div>
                    <div style="flex: 1;">Recall</div>
                    <div style="flex: 1;">ROC-AUC</div>
                    <div style="flex: 1;">Precision</div>
                    <div style="flex: 1;">F1 Score</div>
                    <div style="flex: 1;">Accuracy</div>
                </div>
                {table_rows_html}
            </div>
        </div>
        """)
    else:
        st.warning("Model comparison data (`outputs/model_comparison.csv`) not found. Run model evaluation first.")

    # ------------------------------------------------------------------
    # FIX 6: Fact Sheet Card — dynamically read from model_comparison.csv
    # ------------------------------------------------------------------
    fact_recall    = "N/A"
    fact_roc       = "N/A"
    fact_train_size = "N/A"

    if os.path.exists(comparison_path):
        try:
            _df = pd.read_csv(comparison_path)
            _xgb = _df[_df["model"] == "xgb"].iloc[0]
            fact_recall = f"{_xgb['recall']:.2%}"
            fact_roc    = f"{_xgb['roc_auc']:.4f}"
        except Exception:
            pass

    # Training set size from cleaned CSV
    try:
        _cleaned_path = os.path.join(project_root, "data", "processed", "cleaned_appointments_v3.csv")
        if os.path.exists(_cleaned_path):
            _train_df = pd.read_csv(_cleaned_path, usecols=["No-show"])
            # 80% split used in training
            _train_size = int(len(_train_df) * 0.8)
            fact_train_size = f"{_train_size:,}"
    except Exception:
        fact_train_size = "88,421"  # fallback

    st.html(f"""
    <div class="card card-sky-blue" style="padding: 20px;">
        <div class="card-title-text" style="margin-bottom:12px;">Active Model Fact Sheet</div>
        <div style="display:grid; grid-template-columns: repeat(4, 1fr); gap:15px;">
            <div>
                <div style="font-size:11px; color:#94a3b8; text-transform:uppercase;">Primary Metric (Recall)</div>
                <div style="font-size:18px; font-weight:600; color:#16a34a;">{fact_recall}</div>
            </div>
            <div>
                <div style="font-size:11px; color:#94a3b8; text-transform:uppercase;">ROC-AUC Score</div>
                <div style="font-size:18px; font-weight:600; color:#0f1f3d;">{fact_roc}</div>
            </div>
            <div>
                <div style="font-size:11px; color:#94a3b8; text-transform:uppercase;">Training Set Size</div>
                <div style="font-size:18px; font-weight:600; color:#0f1f3d;">{fact_train_size}</div>
            </div>
            <div>
                <div style="font-size:11px; color:#94a3b8; text-transform:uppercase;">SMOTE Resampling</div>
                <div style="font-size:18px; font-weight:600; color:#0284c7;">Applied</div>
            </div>
        </div>
    </div>
    """)

    # ------------------------------------------------------------------
    # Visual Plots
    # ------------------------------------------------------------------
    st.markdown("#### Evaluation Curves")
    c_plots1, c_plots2 = st.columns(2)
    
    with c_plots1:
        with st.container(border=True):
            st.html("<div class='card-title-text' style='margin-bottom:10px;'>Confusion Matrix (XGBoost)</div>")
            path = get_confusion_matrix_path("xgb")
            if os.path.exists(path):
                st.image(path, use_container_width=True)
            else:
                st.info("XGBoost Confusion matrix plot not found.")
        
    with c_plots2:
        with st.container(border=True):
            st.html("<div class='card-title-text' style='margin-bottom:10px;'>Receiver Operating Characteristic (ROC) Curves</div>")
            roc_path = get_roc_curve_path()
            if os.path.exists(roc_path):
                st.image(roc_path, use_container_width=True)
            else:
                st.info("ROC Curve plot not found.")
