"""Daily Briefing page for CarePredict. Shows only critical cases for today."""

import streamlit as st
import datetime

def render_daily_briefing():
    """Render the Daily Briefing page."""
    st.html("<h3 style='margin:0 0 10px 0; color:#0f1f3d; font-weight:600;'>Daily Briefing</h3>")
    st.html("<p style='color:#64748b; font-size:13px;'>Focused view of today's critical cases needing urgent coordinator outreach.</p>")
    
    if "patients_df" not in st.session_state:
        st.warning("Patient data is initializing...")
        st.stop()
        
    df = st.session_state.patients_df
    contacted = st.session_state.get("contacted_patients", set())
    
    # Filter for today's high risk cases
    today_critical = df[(df["risk_tier"] == "High") & (df["appointment_day"] == "Today")]
    
    # Exclude already contacted if needed, or show them as resolved.
    # To reduce cognitive load, let's show outstanding cases first, and a separate list of resolved cases today!
    outstanding = today_critical[~today_critical["patient_id"].isin(contacted)]
    resolved = today_critical[today_critical["patient_id"].isin(contacted)]
    
    # ------------------------------------------------------------------
    # Outstanding Critical Cases
    # ------------------------------------------------------------------
    st.markdown("#### Outstanding Critical Cases")
    
    if len(outstanding) == 0:
        st.html("""
        <div class="banner banner-success">
            No critical interventions needed today. All high-risk cases have been contacted.
        </div>
        """)
    else:
        # We can render these in a table with a button per row.
        # Streamlit table with buttons is easiest done using a loop and columns or a dataframe with a button column.
        # But we can make it look gorgeous by rendering individual rows with columns.
        for idx, row in outstanding.iterrows():
            pid = row["patient_id"]
            name = row["name"]
            age = row["Age"]
            gender_str = "Female" if row["Gender"] == 0 else "Male"
            prob_percent = int(row["probability"] * 100)
            action = row["recommended_action"]
            
            # Use columns for custom card representation of each patient
            col_info, col_risk, col_action, col_btn = st.columns([3, 2, 2, 1])
            with col_info:
                st.html(f"""
                <div style="font-size:13px; font-weight:600; color:#0f1f3d;">{name}</div>
                <div style="font-size:11px; color:#94a3b8;">ID: {pid} | {age} yrs, {gender_str}</div>
                """)
            with col_risk:
                st.html(f"""
                <div style="font-size:11px; color:#94a3b8; margin-bottom:2px;">No-Show Risk</div>
                <div style="display:flex; align-items:center; gap:6px;">
                    <span class="pill pill-red">High ({prob_percent}%)</span>
                </div>
                """)
            with col_action:
                st.html(f"""
                <div style="font-size:11px; color:#94a3b8; margin-bottom:2px;">Recommended Outreach</div>
                <span class="action-badge action-call-sms">{action}</span>
                """)
            with col_btn:
                if st.button("Mark Contacted", key=f"contact_{pid}", use_container_width=True):
                    # Record contact details
                    contacted.add(pid)
                    st.session_state.contacted_patients = contacted
                    # Save to intervention log session state
                    if "intervention_log" not in st.session_state:
                        st.session_state.intervention_log = []
                    st.session_state.intervention_log.append({
                        "patient_id": pid,
                        "name": name,
                        "action_taken": action,
                        "timestamp": datetime.datetime.now().strftime("%I:%M %p"),
                    })
                    st.toast(f"Outreach logged for {name}.")
                    st.rerun()
            st.html("<hr style='margin:10px 0; border:none; border-top:1px solid #e2e6ed;' />")

    # ------------------------------------------------------------------
    # Resolved Cases Today / Intervention Log
    # ------------------------------------------------------------------
    st.markdown("#### Today's Intervention Log")
    
    log = st.session_state.get("intervention_log", [])
    if not log:
        st.html("<p style='font-size:12px; color:#94a3b8;'>No interventions logged yet today.</p>")
    else:
        # Render log in a clean table using flexbox divs to bypass sanitization
        log_rows = ""
        for entry in reversed(log):
            log_rows += f"""
            <div class="flex-table-row">
                <div style="flex: 2; display: flex; flex-direction: column;">
                    <span style="font-weight: 600; color: #0f1f3d;">{entry['name']}</span>
                    <span style="font-size: 10px; color: #94a3b8;">{entry['patient_id']}</span>
                </div>
                <div style="flex: 1;"><span class="action-badge action-standard">Contacted</span></div>
                <div style="flex: 2; font-size: 12px; color: #374151;">{entry['action_taken']}</div>
                <div style="flex: 1; font-size: 12px; color: #64748b;">{entry['timestamp']}</div>
            </div>
            """
            
        st.html(f"""
        <div class="card" style="padding:15px;">
            <div class="flex-table">
                <div class="flex-table-header">
                    <div style="flex: 2;">Patient</div>
                    <div style="flex: 1;">Status</div>
                    <div style="flex: 2;">Action Performed</div>
                    <div style="flex: 1;">Logged At</div>
                </div>
                {log_rows}
            </div>
        </div>
        """)
