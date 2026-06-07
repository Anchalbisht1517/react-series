"""Dashboard page for CarePredict Hospital Analytics Suite."""

import os
import streamlit as st
import pandas as pd
import numpy as np


def _load_model_metrics():
    """Load XGBoost metrics from model_comparison.csv. Returns a dict or None."""
    try:
        project_root = os.path.abspath(
            os.path.join(os.path.dirname(__file__), "..", "..", "..")
        )
        comparison_path = os.path.join(project_root, "outputs", "model_comparison.csv")
        if os.path.exists(comparison_path):
            df = pd.read_csv(comparison_path)
            xgb = df[df["model"] == "xgb"].iloc[0]
            return {
                "recall":    float(xgb["recall"]),
                "roc_auc":   float(xgb["roc_auc"]),
                "precision": float(xgb["precision"]),
                "f1":        float(xgb["f1"]),
                "accuracy":  float(xgb["accuracy"]),
            }
    except Exception:
        pass
    return None


def render_dashboard():
    """Render the dashboard page."""
    # Ensure patients data is initialized in session state
    if "patients_df" not in st.session_state:
        st.warning("Patient data is initializing...")
        st.stop()

    df = st.session_state.patients_df
    contacted = st.session_state.get("contacted_patients", set())

    # ------------------------------------------------------------------
    # Pre-compute all real counts up front (used in multiple panels)
    # ------------------------------------------------------------------
    total_appts  = len(df)
    high_count   = len(df[df["risk_tier"] == "High"])
    medium_count = len(df[df["risk_tier"] == "Medium"])
    low_count    = len(df[df["risk_tier"] == "Low"])
    flagged_count = high_count + medium_count            # Fix 1 & 5

    flagged_df         = df[df["risk_tier"].isin(["High", "Medium"])]
    not_contacted_count = len(flagged_df[~flagged_df["patient_id"].isin(contacted)])  # Fix 2
    contacted_count     = len(flagged_df[flagged_df["patient_id"].isin(contacted)])   # Fix 2
    medium_sms_count    = len(df[(df["risk_tier"] == "Medium") & (~df["patient_id"].isin(contacted))])  # Fix 2

    # ------------------------------------------------------------------
    # Header & Quick Action Row
    # ------------------------------------------------------------------
    col_header, col_btn = st.columns([5, 1])
    with col_header:
        st.html("<h3 style='margin:0 0 10px 0; color:#0f1f3d; font-weight:600;'>Today's clinic overview</h3>")
    with col_btn:
        if st.button("Quick Assess →", use_container_width=True):
            st.query_params["page"] = "Patient_Risk_Assessment"
            st.rerun()

    # ------------------------------------------------------------------
    # 5 KPI Cards Row
    # ------------------------------------------------------------------
    kpi_cols = st.columns(5)

    # KPI 1: Total Appointments
    with kpi_cols[0]:
        st.html(f"""
        <div class="card card-sky-blue">
            <div class="kpi-title">Total Appts</div>
            <div class="kpi-value">{total_appts}</div>
            <div class="kpi-subtitle">scheduled today</div>
        </div>
        """)

    # KPI 2: Predicted No-Shows (High + Medium risk)
    no_shows = flagged_count
    with kpi_cols[1]:
        st.html(f"""
        <div class="card card-red">
            <div class="kpi-title">Predicted No-Shows</div>
            <div class="kpi-value">{no_shows}</div>
            <div class="kpi-subtitle"><span class="kpi-delta kpi-delta-up-red">↑ {not_contacted_count}</span> still pending</div>
        </div>
        """)

    # KPI 3: Attendance Rate (Low risk / Total)
    attendance_rate = (low_count / total_appts) * 100
    with kpi_cols[2]:
        st.html(f"""
        <div class="card card-teal">
            <div class="kpi-title">Attendance Rate</div>
            <div class="kpi-value">{attendance_rate:.1f}%</div>
            <div class="kpi-subtitle">predicted attendance</div>
        </div>
        """)

    # KPI 4: High-Risk Patients (High risk only)
    with kpi_cols[3]:
        st.html(f"""
        <div class="card card-amber">
            <div class="kpi-title">High-Risk Patients</div>
            <div class="kpi-value">{high_count}</div>
            <div class="kpi-subtitle">need intervention</div>
        </div>
        """)

    # KPI 5: Intervention Rate (contacted flagged / total flagged)
    if flagged_count > 0:
        intervention_rate = (contacted_count / flagged_count) * 100
    else:
        intervention_rate = 0.0

    with kpi_cols[4]:
        st.html(f"""
        <div class="card card-purple">
            <div class="kpi-title">Intervention Rate</div>
            <div class="kpi-value">{intervention_rate:.0f}%</div>
            <div class="kpi-subtitle">{contacted_count} of {flagged_count} contacted</div>
        </div>
        """)

    # ------------------------------------------------------------------
    # Main Dashboard Columns
    # ------------------------------------------------------------------
    col_main, col_side = st.columns([7, 3])

    with col_main:
        # Patient Risk Queue Table
        selected_filter = st.query_params.get("filter", "All")

        # Filter dataframe based on selection
        filtered_df = df.copy()

        if selected_filter == "Call_needed":
            filtered_df = filtered_df[filtered_df["risk_tier"] == "High"]
        elif selected_filter == "SMS_only":
            filtered_df = filtered_df[filtered_df["risk_tier"] == "Medium"]
        elif selected_filter == "Today":
            filtered_df = filtered_df[filtered_df["appointment_day"] == "Today"]
        elif selected_filter == "Tomorrow":
            filtered_df = filtered_df[filtered_df["appointment_day"] == "Tomorrow"]

        # Select first 5 for the dashboard summary view
        display_df = filtered_df.head(5)

        # Build Table HTML
        table_rows_html = ""
        for _, row in display_df.iterrows():
            pid = row["patient_id"]
            name = row["name"]
            age = row["Age"]
            gender_str = "F" if row["Gender"] == 0 else "M"
            prob_percent = int(row["probability"] * 100)

            # Risk Pill Class
            risk_tier = row["risk_tier"]
            if risk_tier == "High":
                pill_class = "pill-red"
                bar_class = "prob-bar-red"
            elif risk_tier == "Medium":
                pill_class = "pill-amber"
                bar_class = "prob-bar-amber"
            else:
                pill_class = "pill-green"
                bar_class = "prob-bar-green"

            # Intervention Badge Class
            action = row["recommended_action"]
            if "Call" in action:
                act_class = "action-call-sms"
            elif "SMS" in action:
                act_class = "action-sms"
            else:
                act_class = "action-standard"

            table_rows_html += f"""
            <div class="flex-table-row">
                <div class="w-pat">
                    <span class="patient-name">{name}</span>
                    <span class="patient-id">{pid}</span>
                </div>
                <div class="w-age">{age}, {gender_str}</div>
                <div class="w-prob">
                    <div class="prob-bar-bg mr-0">
                        <div class="prob-bar-fill {bar_class}" style="width: {prob_percent}%;"></div>
                    </div>
                    <span>{prob_percent}%</span>
                </div>
                <div class="w-risk"><span class="pill {pill_class}">{risk_tier}</span></div>
                <div class="w-interv"><span class="action-badge {act_class}">{action}</span></div>
            </div>
            """

        def _chip_cls(f_val):
            return "filter-chip active" if selected_filter == f_val else "filter-chip"

        chips_html = f"""
        <div class="filter-chips-container" style="display:flex; gap:8px; margin-bottom:16px;">
            <a href="?page=Dashboard&filter=All" target="_self" class="{_chip_cls('All')}" style="text-decoration:none;">All</a>
            <a href="?page=Dashboard&filter=Call_needed" target="_self" class="{_chip_cls('Call_needed')}" style="text-decoration:none;">Call needed</a>
            <a href="?page=Dashboard&filter=SMS_only" target="_self" class="{_chip_cls('SMS_only')}" style="text-decoration:none;">SMS only</a>
            <a href="?page=Dashboard&filter=Today" target="_self" class="{_chip_cls('Today')}" style="text-decoration:none;">Today</a>
            <a href="?page=Dashboard&filter=Tomorrow" target="_self" class="{_chip_cls('Tomorrow')}" style="text-decoration:none;">Tomorrow</a>
        </div>
        """

        # FIX 5: Dynamic high_count in "View all X →" link
        st.html(f"""
        <div class="card card-large">
            <div class="card-header-container" style="margin-bottom: 12px;">
                <div class="card-title-text">High-risk patient queue</div>
                <a href="/?page=Risk_Queue" target="_self" class="card-action-link">View all {high_count} →</a>
            </div>
            {chips_html}
            <div class="flex-table">
                <div class="flex-table-header">
                    <div class="w-pat">Patient</div>
                    <div class="w-age">Age</div>
                    <div class="w-prob">No-show prob.</div>
                    <div class="w-risk">Risk</div>
                    <div class="w-interv">Intervention</div>
                </div>
                {table_rows_html if table_rows_html else '<div style="text-align:center; color:#94a3b8; padding:20px; font-size:12px;">No patients match this filter.</div>'}
            </div>
        </div>
        """)

    with col_side:
        # ------------------------------------------------------------------
        # FIX 1: Risk Distribution Donut — dynamic counts + dynamic gradient
        # ------------------------------------------------------------------
        # Compute conic-gradient stops from real counts
        high_pct   = (high_count   / total_appts) * 100
        medium_pct = (medium_count / total_appts) * 100
        # High = red, Medium = amber, Low = green
        high_stop   = high_pct
        medium_stop = high_pct + medium_pct

        st.html(f"""
        <style>
            .donut-gauge-dynamic {{
                width: 130px;
                height: 130px;
                border-radius: 50%;
                background: conic-gradient(
                    #dc2626 0% {high_stop:.1f}%,
                    #f59e0b {high_stop:.1f}% {medium_stop:.1f}%,
                    #16a34a {medium_stop:.1f}% 100%
                );
                display: flex;
                align-items: center;
                justify-content: center;
                position: relative;
            }}
        </style>
        <div class="card" style="padding: 20px;">
            <div class="card-title-text" style="margin-bottom:15px;">Risk distribution</div>
            <div class="gauge-wrapper">
                <div class="donut-gauge-dynamic">
                    <div class="donut-hole-center">
                        <div class="gauge-value">{flagged_count}</div>
                        <div class="gauge-label">flagged</div>
                    </div>
                </div>
            </div>
            <div style="margin-top: 15px;">
                <div style="display:flex; justify-content:space-between; font-size:12px; margin-bottom:6px;">
                    <div style="display:flex; align-items:center; gap:6px;">
                        <span style="width:10px; height:10px; background-color:#dc2626; border-radius:50%; display:inline-block;"></span>
                        <span style="color:#64748b;">High risk</span>
                    </div>
                    <span style="font-weight:600; color:#0f1f3d;">{high_count}</span>
                </div>
                <div style="display:flex; justify-content:space-between; font-size:12px; margin-bottom:6px;">
                    <div style="display:flex; align-items:center; gap:6px;">
                        <span style="width:10px; height:10px; background-color:#f59e0b; border-radius:50%; display:inline-block;"></span>
                        <span style="color:#64748b;">Medium risk</span>
                    </div>
                    <span style="font-weight:600; color:#0f1f3d;">{medium_count}</span>
                </div>
                <div style="display:flex; justify-content:space-between; font-size:12px;">
                    <div style="display:flex; align-items:center; gap:6px;">
                        <span style="width:10px; height:10px; background-color:#16a34a; border-radius:50%; display:inline-block;"></span>
                        <span style="color:#64748b;">Low risk</span>
                    </div>
                    <span style="font-weight:600; color:#0f1f3d;">{low_count}</span>
                </div>
            </div>
        </div>
        """)

        # ------------------------------------------------------------------
        # FIX 2: Live Alerts — real computed values
        # ------------------------------------------------------------------
        # Alert 1: how many flagged patients haven't been contacted yet
        alert1_color = "alert-dot-red" if not_contacted_count > 0 else "alert-dot-green"
        alert1_text = (
            f"{not_contacted_count} flagged patients not yet contacted"
            if not_contacted_count > 0
            else "All flagged patients contacted today"
        )

        # Alert 2: how many Medium-risk patients are queued for SMS
        alert2_text = f"{medium_sms_count} medium-risk patients queued for SMS"
        alert2_color = "alert-dot-amber"

        # Alert 3: intervention log activity count
        log_count = len(st.session_state.get("intervention_log", []))
        alert3_text = (
            f"{log_count} outreach action{'s' if log_count != 1 else ''} logged this session"
            if log_count > 0
            else "No outreach actions logged yet this session"
        )

        st.html(f"""
        <div class="card" style="padding: 20px;">
            <div class="card-title-text" style="margin-bottom:15px;">Live alerts</div>
            <div class="alert-item">
                <span class="alert-dot {alert1_color}"></span>
                <div class="alert-content">
                    <span class="alert-text">{alert1_text}</span>
                    <span class="alert-time">Live</span>
                </div>
            </div>
            <div class="alert-item">
                <span class="alert-dot {alert2_color}"></span>
                <div class="alert-content">
                    <span class="alert-text">{alert2_text}</span>
                    <span class="alert-time">Live</span>
                </div>
            </div>
            <div class="alert-item" style="margin-bottom:0;">
                <span class="alert-dot alert-dot-blue"></span>
                <div class="alert-content">
                    <span class="alert-text">{alert3_text}</span>
                    <span class="alert-time">Live</span>
                </div>
            </div>
        </div>
        """)

    # ------------------------------------------------------------------
    # Bottom Row of 3 Columns
    # ------------------------------------------------------------------
    col_perf, col_shap, col_interv = st.columns(3)

    # ------------------------------------------------------------------
    # FIX 4: Model Performance Snapshot — read from model_comparison.csv
    # ------------------------------------------------------------------
    with col_perf:
        metrics = _load_model_metrics()
        if metrics:
            recall_str    = f"{metrics['recall']:.2%}"
            roc_str       = f"{metrics['roc_auc']:.4f}"
            precision_str = f"{metrics['precision']:.2%}"
            f1_str        = f"{metrics['f1']:.4f}"
            accuracy_str  = f"{metrics['accuracy']:.2%}"
        else:
            # Graceful fallback (should rarely happen)
            recall_str    = "N/A"
            roc_str       = "N/A"
            precision_str = "N/A"
            f1_str        = "N/A"
            accuracy_str  = "N/A"

        st.html(f"""
        <div class="card" style="min-height: 320px; padding: 20px;">
            <div class="card-title-text" style="margin-bottom:15px;">Model performance snapshot</div>
            <div style="display:flex; justify-content:space-between; font-size:12px; margin-bottom:8px; border-bottom:1px solid #f8fafc; padding-bottom:6px;">
                <span style="color:#64748b;">Recall (XGBoost)</span>
                <span style="font-weight:600; color:#16a34a;">{recall_str}</span>
            </div>
            <div style="display:flex; justify-content:space-between; font-size:12px; margin-bottom:8px; border-bottom:1px solid #f8fafc; padding-bottom:6px;">
                <span style="color:#64748b;">ROC-AUC</span>
                <span style="font-weight:600; color:#0f1f3d;">{roc_str}</span>
            </div>
            <div style="display:flex; justify-content:space-between; font-size:12px; margin-bottom:8px; border-bottom:1px solid #f8fafc; padding-bottom:6px;">
                <span style="color:#64748b;">Precision</span>
                <span style="font-weight:600; color:#0f1f3d;">{precision_str}</span>
            </div>
            <div style="display:flex; justify-content:space-between; font-size:12px; margin-bottom:8px; border-bottom:1px solid #f8fafc; padding-bottom:6px;">
                <span style="color:#64748b;">F1 score</span>
                <span style="font-weight:600; color:#0f1f3d;">{f1_str}</span>
            </div>
            <div style="display:flex; justify-content:space-between; font-size:12px; margin-bottom:8px; border-bottom:1px solid #f8fafc; padding-bottom:6px;">
                <span style="color:#64748b;">Accuracy</span>
                <span style="font-weight:600; color:#0f1f3d;">{accuracy_str}</span>
            </div>
            <div style="display:flex; justify-content:space-between; font-size:12px; margin-bottom:0;">
                <span style="color:#64748b;">SMOTE applied</span>
                <span style="font-weight:600; color:#0284c7;">Yes</span>
            </div>
        </div>
        """)

    # ------------------------------------------------------------------
    # FIX 3: No-show drivers (SHAP) — REAL values from XGBoost TreeExplainer
    # Values computed on 500-sample subset; grouped by conceptual feature:
    #   days_waiting:       1.0813  (top driver — wait time)
    #   Neighbourhood:      0.6754  (location-based risk)
    #   Age:                0.2864  (patient demographics)
    #   SMS_received:       0.1372  (intervention signal)
    #   previous_no_shows:  0.0694  (history)
    #   appointment_weekday:0.0592  (scheduling pattern)
    # Bar widths are normalized to the max value (days_waiting = 100%)
    # ------------------------------------------------------------------
    with col_shap:
        # Real SHAP values (mean |SHAP|) from model computation
        shap_features = [
            ("Days Waiting",         1.0813, "#0284c7"),   # scheduling — blue
            ("Neighbourhood",        0.6754, "#a855f7"),   # location — purple
            ("Age",                  0.2864, "#a855f7"),   # demographics — purple
            ("SMS Received",         0.1372, "#16a34a"),   # intervention — teal
            ("Prev. No-Shows",       0.0694, "#0284c7"),   # history — blue
            ("Appt. Weekday",        0.0592, "#94a3b8"),   # scheduling — gray
        ]
        max_val = shap_features[0][1]  # days_waiting is the max

        shap_bars_html = ""
        for i, (fname, val, color) in enumerate(shap_features):
            bar_width = int((val / max_val) * 100)
            mb = "0" if i == len(shap_features) - 1 else "10px"
            shap_bars_html += f"""
            <div style="margin-bottom: {mb};">
                <div style="display:flex; justify-content:space-between; font-size:11px; margin-bottom:2px;">
                    <span style="color:#475569;">{fname}</span>
                    <span style="font-weight:500; color:#0f1f3d;">{val:.4f}</span>
                </div>
                <div style="width:100%; height:8px; background-color:#f1f5f9; border-radius:4px; overflow:hidden;">
                    <div style="width:{bar_width}%; height:100%; background-color:{color}; border-radius:4px;"></div>
                </div>
            </div>
            """

        st.html(f"""
        <div class="card" style="min-height: 320px; padding: 20px;">
            <div class="card-title-text" style="margin-bottom:4px;">No-show drivers (SHAP)</div>
            <div style="font-size:10px; color:#94a3b8; margin-bottom:12px;">Mean |SHAP| value — XGBoost on 500-sample subset</div>
            {shap_bars_html}
        </div>
        """)

    # Bottom 3: Upcoming Interventions — dynamic from real session data
    with col_interv:
        # Pull real high-risk today patients from session state
        today_high = df[
            (df["risk_tier"].isin(["High", "Medium"])) &
            (df["appointment_day"].isin(["Today", "Tomorrow"]))
        ].sort_values(by=["appointment_day", "probability"], ascending=[True, False]).head(4)

        timeline_items_html = ""
        for i, (_, row) in enumerate(today_high.iterrows()):
            name = row["name"]
            pid  = row["patient_id"]
            day  = row["appointment_day"]
            tier = row["risk_tier"]
            action = row["recommended_action"]

            if day == "Today":
                dot_class   = "alert-dot-red"
                badge_time  = "Today"
            else:
                dot_class   = "alert-dot-amber" if tier == "High" else "alert-dot-green"
                badge_time  = "Tomorrow"

            if "Call" in action:
                act_class = "action-call-sms"
                act_label = "Call + SMS"
            elif "SMS" in action:
                act_class = "action-sms"
                act_label = "SMS reminder"
            else:
                act_class = "action-standard"
                act_label = "No action"

            border_style = "border-bottom:none; padding-bottom:0;" if i == len(today_high) - 1 else ""

            timeline_items_html += f"""
            <div class="timeline-item" style="{border_style}">
                <div class="timeline-left">
                    <span class="alert-dot {dot_class}" style="margin-top:2px;"></span>
                    <div class="timeline-info">
                        <span class="timeline-name">{name} — {pid}</span>
                        <span class="timeline-appt">Appt {day.lower()}</span>
                    </div>
                </div>
                <div class="timeline-right">
                    <span class="timeline-badge-time">{badge_time}</span>
                    <span class="action-badge {act_class}">{act_label}</span>
                </div>
            </div>
            """

        if not timeline_items_html:
            timeline_items_html = "<p style='font-size:12px; color:#94a3b8;'>No upcoming high-risk appointments.</p>"

        st.html(f"""
        <div class="card" style="min-height: 320px; padding: 20px;">
            <div class="card-title-text" style="margin-bottom:10px;">Upcoming interventions</div>
            {timeline_items_html}
        </div>
        """)
