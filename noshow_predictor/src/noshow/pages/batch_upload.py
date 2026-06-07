"""Batch Upload page for CarePredict. Upgrades bulk predictions to priority queues."""

import streamlit as st
import pandas as pd
import datetime
from noshow.pipeline.prediction_pipeline import PredictionPipeline
from noshow.exception import NoShowException

def render_batch_upload():
    """Render the Batch Upload page."""
    st.html("<h3 style='margin:0 0 10px 0; color:#0f1f3d; font-weight:600;'>Batch Upload</h3>")
    st.html("<p style='color:#64748b; font-size:13px;'>Upload bulk patient rosters to analyze and prioritize outreach lists.</p>")
    
    st.html("""
    <div class="card" style="padding:15px; margin-bottom:20px;">
        <b>Expected columns</b>: <code>Age</code>, <code>Gender</code> (0=F, 1=M), <code>Scholarship</code> (0/1), 
        <code>Hypertension</code> (0/1), <code>Diabetes</code> (0/1), <code>Alcoholism</code> (0/1), 
        <code>Handicap</code> (0-4), <code>SMS_received</code> (0/1), <code>days_waiting</code>, 
        <code>appointment_weekday</code> (0-6), <code>previous_no_shows</code>, <code>Neighbourhood</code>.
    </div>
    """)

    uploaded_file = st.file_uploader("Choose a CSV file containing patient data", type="csv")
    
    if uploaded_file is not None:
        try:
            # We want to cache predictions so we don't rerun on every click of 'Mark Contacted'
            if "last_batch_name" not in st.session_state or st.session_state.last_batch_name != uploaded_file.name:
                input_df = pd.read_csv(uploaded_file)
                
                with st.spinner("Running batch predictions..."):
                    pipeline = PredictionPipeline()
                    results_df = pipeline.predict_batch(input_df)
                
                # Check for patient name and ID columns, if missing, generate them
                if "patient_id" not in results_df.columns:
                    # Create mock IDs
                    results_df["patient_id"] = [f"APT-{1000 + i}" for i in range(len(results_df))]
                if "name" not in results_df.columns:
                    # Mock names
                    first_names = ["Emma", "Noah", "Olivia", "Liam", "Ava", "William", "Sophia", "Mason", "Isabella", "James"]
                    last_initials = ["S.", "O.", "K.", "B.", "T.", "M.", "H.", "L.", "R.", "W."]
                    results_df["name"] = [
                        f"{first_names[i % len(first_names)]} {last_initials[(i + 3) % len(last_initials)]}" 
                        for i in range(len(results_df))
                    ]
                    
                st.session_state.last_batch_name = uploaded_file.name
                st.session_state.last_batch_df = results_df
                st.toast("Batch assessment completed successfully.", icon="📁")

            # Load from cache
            results_df = st.session_state.last_batch_df
            contacted = st.session_state.get("contacted_patients", set())
            
            # Auto-scroll helper: anchor target
            st.html("<div id='results-view'></div>")
            
            # Summary Metrics Row
            st.markdown("#### Batch Summary")
            tier_counts = results_df["risk_tier"].value_counts()
            c1, c2, c3, c4 = st.columns(4)
            c1.metric("High Risk (>0.65)", f"{tier_counts.get('High', 0)}")
            c2.metric("Medium Risk (0.40 - 0.65)", f"{tier_counts.get('Medium', 0)}")
            c3.metric("Low Risk (<0.40)", f"{tier_counts.get('Low', 0)}")
            
            # Download results
            csv = results_df.to_csv(index=False).encode("utf-8")
            c4.download_button(
                label="📥 Download Results CSV",
                data=csv,
                file_name="batch_predictions_results.csv",
                mime="text/csv",
                use_container_width=True
            )
            
            st.html("<hr style='margin:15px 0; border:none; border-top:1px solid #e2e6ed;' />")
            
            # High Risk Priority Queue (sorted by probability desc)
            st.markdown("#### High-Risk Priority Queue")
            high_risk_df = results_df[results_df["risk_tier"] == "High"].sort_values(by="probability", ascending=False)
            
            if len(high_risk_df) == 0:
                st.html("""
                <div class="banner banner-success">
                    No high-risk (>0.65) patients found in this batch!
                </div>
                """)
            else:
                st.html("<p style='font-size:12px; color:#64748b; margin-top:-5px;'>These patients require immediate phone calls and text follow-ups.</p>")
                
                # Render priority queue with active contacting buttons
                for idx, row in high_risk_df.iterrows():
                    pid = row["patient_id"]
                    name = row["name"]
                    age = row["Age"]
                    gender_str = "Female" if row["Gender"] == 0 else "Male"
                    prob = row["probability"]
                    action = row["recommended_action"]
                    
                    is_contacted = pid in contacted
                    
                    col_info, col_prob, col_action, col_btn = st.columns([3, 2, 2, 1])
                    with col_info:
                        st.html(f"""
                        <div style="font-size:13px; font-weight:600; color:{'#94a3b8' if is_contacted else '#0f1f3d'};">
                            {name} {f'✓' if is_contacted else ''}
                        </div>
                        <div style="font-size:11px; color:#94a3b8;">ID: {pid} | {age} yrs, {gender_str}</div>
                        """)
                    with col_prob:
                        st.html(f"""
                        <div style="font-size:11px; color:#94a3b8; margin-bottom:2px;">Risk Probability</div>
                        <span class="pill {'pill-green' if is_contacted else 'pill-red'}">{prob:.1%}</span>
                        """)
                    with col_action:
                        st.html(f"""
                        <div style="font-size:11px; color:#94a3b8; margin-bottom:2px;">Intervention Type</div>
                        <span class="action-badge {'action-standard' if is_contacted else 'action-call-sms'}">{action}</span>
                        """)
                    with col_btn:
                        if is_contacted:
                            st.button("Contacted", key=f"btn_batch_{pid}", disabled=True, use_container_width=True)
                        else:
                            if st.button("Mark Contacted", key=f"btn_batch_{pid}", use_container_width=True):
                                contacted.add(pid)
                                st.session_state.contacted_patients = contacted
                                # Append to intervention log
                                if "intervention_log" not in st.session_state:
                                    st.session_state.intervention_log = []
                                st.session_state.intervention_log.append({
                                    "patient_id": pid,
                                    "name": name,
                                    "action_taken": action,
                                    "timestamp": datetime.datetime.now().strftime("%I:%M %p"),
                                })
                                st.toast(f"Contact logged for {name}.")
                                st.rerun()
                    st.html("<hr style='margin:10px 0; border:none; border-top:1px solid #e2e6ed;' />")
            
            # Complete Batch Results Preview Table
            with st.expander("Show Complete Roster Preview"):
                st.dataframe(results_df[["patient_id", "name", "Age", "Gender", "probability", "risk_tier", "recommended_action"]], use_container_width=True)
                
        except NoShowException as e:
            st.error(f"Pipeline error: {e}")
            st.info("Make sure the model preprocessor and xgboost model files exist.")
        except Exception as e:
            st.error(f"Unexpected error: {e}")
            
    else:
        # Empty State
        st.html("""
        <div style="display:flex; flex-direction:column; align-items:center; justify-content:center; height:300px; border:1px dashed #e2e6ed; border-radius:8px; background-color:#ffffff; color:#94a3b8; padding:20px; text-align:center;">
            <h5 style="margin:10px 0 5px 0; color:#64748b;">Upload a CSV File</h5>
            <p style="font-size:12px; margin:0; color:#94a3b8;">Choose a structured patient record CSV sheet to evaluate appointments in batch.</p>
        </div>
        """)
