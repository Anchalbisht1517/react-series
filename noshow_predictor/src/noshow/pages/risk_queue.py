"""Risk Queue page for CarePredict. Displays complete queue of flagged patients."""

import streamlit as st
import pandas as pd
import datetime

def render_risk_queue():
    """Render the Risk Queue page."""
    st.html("<h3 style='margin:0 0 10px 0; color:#0f1f3d; font-weight:600;'>Risk Queue</h3>")
    st.html("<p style='color:#64748b; font-size:13px;'>Manage outstanding no-show risk interventions for flagged patients.</p>")
    
    if "patients_df" not in st.session_state:
        st.warning("Patient data is initializing...")
        st.stop()
        
    df = st.session_state.patients_df
    contacted = st.session_state.get("contacted_patients", set())
    
    # ------------------------------------------------------------------
    # Filters & Search
    # ------------------------------------------------------------------
    col_search, col_filter = st.columns([2, 1])
    with col_search:
        search_query = st.text_input("🔍 Search patient name or ID...", value="")
    with col_filter:
        status_filter = st.selectbox("Status", ["All Flagged", "Action Needed (Pending)", "Contacted (Resolved)"])
        
    # Get all flagged (High + Medium risk) patients
    flagged_df = df[df["risk_tier"].isin(["High", "Medium"])].copy()
    
    # Apply search filter
    if search_query:
        flagged_df = flagged_df[
            flagged_df["name"].str.contains(search_query, case=False, na=False) |
            flagged_df["patient_id"].str.contains(search_query, case=False, na=False)
        ]
        
    # Apply status filter
    if status_filter == "Action Needed (Pending)":
        flagged_df = flagged_df[~flagged_df["patient_id"].isin(contacted)]
    elif status_filter == "Contacted (Resolved)":
        flagged_df = flagged_df[flagged_df["patient_id"].isin(contacted)]
        
    # Total outstanding
    outstanding_count = len(flagged_df[~flagged_df["patient_id"].isin(contacted)])
    
    st.html(f"""
    <div style="font-size:12px; color:#64748b; margin-bottom:15px;">
        Showing <b>{len(flagged_df)}</b> flagged patients | <b>{outstanding_count}</b> outstanding actions pending.
    </div>
    """)
    
    # ------------------------------------------------------------------
    # Queue Table
    # ------------------------------------------------------------------
    if len(flagged_df) == 0:
        st.html("""
        <div style="display:flex; flex-direction:column; align-items:center; justify-content:center; height:200px; border:1px dashed #e2e6ed; border-radius:8px; background-color:#ffffff; color:#94a3b8; padding:20px; text-align:center;">
            <p style="font-size:13px; color:#64748b; font-weight:500;">No flagged patients found matching this filter.</p>
        </div>
        """)
    else:
        # We'll render an interactive table using a list of rows with mark contacted buttons.
        # It's cleaner to render a nice clinical card grid or a list of items for high-fidelity look.
        # Let's render them as rows in a list inside a card
        with st.container(border=True):
            for idx, row in flagged_df.iterrows():
                pid = row["patient_id"]
                name = row["name"]
                age = row["Age"]
                gender_str = "Female" if row["Gender"] == 0 else "Male"
                prob_percent = int(row["probability"] * 100)
                action = row["recommended_action"]
                tier = row["risk_tier"]
                day = row["appointment_day"]
                
                is_contacted = pid in contacted
                
                # Setup layouts
                col_pat, col_stats, col_act, col_button = st.columns([3, 2, 2, 1])
                with col_pat:
                    st.html(f"""
                    <div style="font-size:13px; font-weight:600; color:{'#94a3b8' if is_contacted else '#0f1f3d'};">
                        {name} {f'✓' if is_contacted else ''}
                    </div>
                    <div style="font-size:11px; color:#94a3b8;">ID: {pid} | {age} yrs, {gender_str} | Appt: {day}</div>
                    """)
                with col_stats:
                    st.html(f"""
                    <div style="font-size:11px; color:#94a3b8; margin-bottom:2px;">Risk & Probability</div>
                    <span class="pill {'pill-green' if is_contacted else 'pill-red' if tier == 'High' else 'pill-amber'}">
                        {tier} ({prob_percent}%)
                    </span>
                    """)
                with col_act:
                    st.html(f"""
                    <div style="font-size:11px; color:#94a3b8; margin-bottom:2px;">Outreach Action</div>
                    <span class="action-badge {'action-standard' if is_contacted else 'action-call-sms' if tier == 'High' else 'action-sms'}">
                        {action}
                    </span>
                    """)
                with col_button:
                    if is_contacted:
                        st.button("Contacted", key=f"btn_q_{pid}", disabled=True, use_container_width=True)
                    else:
                        if st.button("Mark Contacted", key=f"btn_q_{pid}", use_container_width=True):
                            contacted.add(pid)
                            st.session_state.contacted_patients = contacted
                            # Append to log
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
