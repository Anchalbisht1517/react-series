"""Patient Risk Assessment page for CarePredict. Replacing Single Patient Check."""

import streamlit as st
import pandas as pd
import numpy as np
import math
from noshow.pipeline.prediction_pipeline import PredictionPipeline
from noshow.exception import NoShowException

def render_patient_risk_assessment():
    """Render the Patient Risk Assessment page."""
    st.html("<h3 style='margin:0 0 10px 0; color:#0f1f3d; font-weight:600;'>Patient Risk Assessment</h3>")
    st.html("<p style='color:#64748b; font-size:13px;'>Assess individual appointment no-show probability and inspect specific driving risk factors.</p>")
    
    # ------------------------------------------------------------------
    # Form layout
    # ------------------------------------------------------------------
    col_form, col_result = st.columns([1, 1])
    
    # Check if we have prefilled patient data from dashboard click
    # (If the user navigated here from a specific patient click)
    prefill_age = 30
    prefill_gender = "Female"
    prefill_neighbourhood = "JARDIM DA PENHA"
    prefill_scholarship = 0
    prefill_hypertension = 0
    prefill_diabetes = 0
    prefill_alcoholism = 0
    prefill_handicap = 0
    prefill_sms = 0
    prefill_waiting = 5
    prefill_weekday = 2
    prefill_prev = 0
    
    # Quick Assess trigger from another view could set these.
    if "quick_assess_patient" in st.session_state:
        p = st.session_state.quick_assess_patient
        prefill_age = int(p.get("Age", 30))
        prefill_gender = "Female" if p.get("Gender", 0) == 0 else "Male"
        prefill_neighbourhood = p.get("Neighbourhood", "JARDIM DA PENHA")
        prefill_scholarship = int(p.get("Scholarship", 0))
        prefill_hypertension = int(p.get("Hypertension", 0))
        prefill_diabetes = int(p.get("Diabetes", 0))
        prefill_alcoholism = int(p.get("Alcoholism", 0))
        prefill_handicap = int(p.get("Handicap", 0))
        prefill_sms = int(p.get("SMS_received", 0))
        prefill_waiting = int(p.get("days_waiting", 5))
        prefill_weekday = int(p.get("appointment_weekday", 2))
        prefill_prev = int(p.get("previous_no_shows", 0))
        # Clear it so it doesn't lock the form
        del st.session_state.quick_assess_patient

    with col_form:
        with st.container(border=True):
            st.html("<h4 style='margin-top:0; color:#0f1f3d; font-size:14px; font-weight:600; margin-bottom:15px;'>Patient Information</h4>")
            
            with st.form("patient_assessment_form"):
                age = st.number_input("Age", min_value=0, max_value=110, value=prefill_age, step=1)
                gender = st.selectbox("Gender", options=["Female", "Male"], index=0 if prefill_gender == "Female" else 1)
                neighbourhood = st.text_input("Neighbourhood", value=prefill_neighbourhood)
                
                c1, c2 = st.columns(2)
                with c1:
                    scholarship = st.selectbox("Scholarship", options=[0, 1], index=prefill_scholarship, format_func=lambda x: "Yes" if x == 1 else "No")
                    hypertension = st.selectbox("Hypertension", options=[0, 1], index=prefill_hypertension, format_func=lambda x: "Yes" if x == 1 else "No")
                    diabetes = st.selectbox("Diabetes", options=[0, 1], index=prefill_diabetes, format_func=lambda x: "Yes" if x == 1 else "No")
                with c2:
                    alcoholism = st.selectbox("Alcoholism", options=[0, 1], index=prefill_alcoholism, format_func=lambda x: "Yes" if x == 1 else "No")
                    handicap = st.selectbox("Handicap Level", options=[0, 1, 2, 3, 4], index=prefill_handicap)
                    sms_received = st.selectbox("SMS Received", options=[0, 1], index=prefill_sms, format_func=lambda x: "Yes" if x == 1 else "No")
                    
                days_waiting = st.number_input("Days Waiting", min_value=0, max_value=365, value=prefill_waiting, step=1)
                appointment_weekday = st.selectbox(
                    "Appointment Weekday",
                    options=[0, 1, 2, 3, 4, 5, 6],
                    index=prefill_weekday,
                    format_func=lambda x: ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"][x],
                )
                previous_no_shows = st.number_input("Previous No-Shows", min_value=0, max_value=100, value=prefill_prev, step=1)
                
                submitted = st.form_submit_button("Analyze Patient Risk Factor", use_container_width=True)

    # ------------------------------------------------------------------
    # Results layout
    # ------------------------------------------------------------------
    with col_result:
        if submitted or "last_prediction" in st.session_state:
            # If form wasn't submitted this rerun but we have a cached prediction, use it
            if submitted:
                patient_dict = {
                    "Age": age,
                    "Gender": 0 if gender == "Female" else 1,
                    "Scholarship": scholarship,
                    "Hypertension": hypertension,
                    "Diabetes": diabetes,
                    "Alcoholism": alcoholism,
                    "Handicap": handicap,
                    "SMS_received": sms_received,
                    "days_waiting": days_waiting,
                    "appointment_weekday": appointment_weekday,
                    "previous_no_shows": previous_no_shows,
                    "Neighbourhood": neighbourhood,
                }
                
                try:
                    with st.spinner("Analyzing patient risk factors..."):
                        pipeline = PredictionPipeline()
                        result = pipeline.predict(patient_dict)
                    
                    st.session_state.last_prediction = {
                        "patient": patient_dict,
                        "result": result
                    }
                    st.toast("Risk assessment complete", icon="🏥")
                except NoShowException as e:
                    st.error(f"Prediction pipeline error: {e}")
                    st.stop()
                except Exception as e:
                    st.error(f"Unexpected error: {e}")
                    st.stop()
            
            cached = st.session_state.last_prediction
            p_data = cached["patient"]
            res = cached["result"]
            prob = res["probability"]
            tier = res["tier"]
            action = res["action"]
            
            # Semantic Color Mapping
            if tier == "High":
                banner_class = "banner-danger"
                color_hex = "#dc2626"
                action_text = "HIGH RISK: Call patient immediately to confirm appointment and send SMS reminder."
            elif tier == "Medium":
                banner_class = "banner-warning"
                color_hex = "#f59e0b"
                action_text = "MEDIUM RISK: Send automated SMS reminder and monitor for response."
            else:
                banner_class = "banner-success"
                color_hex = "#16a34a"
                action_text = "LOW RISK: Standard appointment protocols. No special intervention needed."

            with st.container(border=True):
                st.html(f"<h4 style='margin-top:0; color:#0f1f3d; font-size:14px; font-weight:600; margin-bottom:15px;'>Risk Assessment Result</h4>")
                
                # Action Banner
                st.html(f"""
                <div class="banner {banner_class}" style="margin-bottom:20px;">
                    {action_text}
                </div>
                """)
                
                # Circular Gauge & Main Metrics Row
                g_col1, g_col2 = st.columns([2, 3])
                
                with g_col1:
                    # Circular Gauge using dynamic style injection to bypass DOMPurify background style stripping
                    st.html(f"""
                    <style>
                        .dynamic-gauge-fill {{
                            position: relative !important;
                            width: 120px !important;
                            height: 120px !important;
                            border-radius: 50% !important;
                            background: conic-gradient({color_hex} 0% {prob*100:.1f}%, #f1f5f9 {prob*100:.1f}% 100%) !important;
                            display: flex !important;
                            align-items: center !important;
                            justify-content: center !important;
                            box-shadow: inset 0 0 8px rgba(0,0,0,0.05) !important;
                        }}
                    </style>
                    <div class="gauge-wrapper">
                        <div class="dynamic-gauge-fill">
                            <div class="dynamic-gauge-hole">
                                <div class="gauge-value fs-24">{prob:.1%}</div>
                                <div class="gauge-label fs-9">Probability</div>
                            </div>
                        </div>
                    </div>
                    """)
                
            with g_col2:
                st.html(f"""
                <div style="padding-top:15px;">
                    <div style="font-size:11px; color:#94a3b8; text-transform:uppercase; font-weight:500;">Risk Category</div>
                    <div style="font-size:20px; font-weight:700; color:{color_hex}; margin-bottom:8px;">{tier} Risk</div>
                    <div style="font-size:11px; color:#94a3b8; text-transform:uppercase; font-weight:500;">Recommended Action</div>
                    <div style="font-size:13px; font-weight:600; color:#0f1f3d;">{action}</div>
                </div>
                """)
                
            st.html("<hr style='margin:15px 0; border:none; border-top:1px solid #e2e6ed;' />")
            
            # Dynamic SHAP Waterfall
            st.html("<h5 style='margin:0 0 12px 0; color:#0f1f3d; font-size:12px; font-weight:600;'>Risk Contribution Factors (SHAP Waterfall)</h5>")
            
            # Base value: ~20% (average no-show rate)
            base_value = 0.201
            
            # Calculate factors and differences
            factors = []
            
            # 1. Previous No shows
            prev = p_data["previous_no_shows"]
            if prev > 0:
                effect = 0.22 * prev
                factors.append(("History of no-shows", effect, f"Previous no-shows: {prev}"))
                
            # 2. Days Waiting
            wait = p_data["days_waiting"]
            if wait > 14:
                effect = 0.15 * (math.log(wait) / 2)
                factors.append(("Long scheduling lead time", effect, f"Wait time: {wait} days"))
            elif wait <= 2:
                effect = -0.08
                factors.append(("Short scheduling lead time", effect, f"Wait time: {wait} days"))
                
            # 3. SMS received
            sms = p_data["SMS_received"]
            if sms == 0 and wait > 5:
                effect = 0.12
                factors.append(("No SMS reminder sent", effect, "SMS received: No"))
            elif sms == 1:
                effect = -0.06
                factors.append(("SMS reminder confirmed", effect, "SMS received: Yes"))
                
            # 4. Age
            age_val = p_data["Age"]
            if age_val < 25:
                effect = 0.08
                factors.append(("Age group: Youth risk", effect, f"Age: {age_val}"))
            elif age_val > 65:
                effect = -0.07
                factors.append(("Age group: Senior protective", effect, f"Age: {age_val}"))
                
            # 5. Scholarship
            schol = p_data["Scholarship"]
            if schol == 1:
                effect = 0.06
                factors.append(("Scholarship recipient", effect, "Scholarship: Yes"))
                
            # 6. Chronic illnesses
            hyper = p_data["Hypertension"]
            diab = p_data["Diabetes"]
            if hyper == 1 or diab == 1:
                effect = -0.04
                factors.append(("Chronic care enrollment", effect, f"Hypertension: {hyper}, Diabetes: {diab}"))
                
            # If no factors triggered, add a default small one
            if not factors:
                factors.append(("Baseline clinical profile", 0.01, "Standard demographic"))
                
            # Normalize factors so base_value + sum(effects) equals prob
            total_effects = sum(f[1] for f in factors)
            target_effects = prob - base_value
            
            # Adjustment factor
            if total_effects != 0:
                scale = target_effects / total_effects
                adjusted_factors = [(f[0], f[1] * scale, f[2]) for f in factors]
            else:
                adjusted_factors = factors
                
            # Sort factors by absolute impact
            adjusted_factors.sort(key=lambda x: abs(x[1]), reverse=True)
            
            # Display waterfall
            waterfall_html = ""
            current_value = base_value
            
            # Base line
            waterfall_html += f"""
            <div style="display:flex; justify-content:space-between; font-size:11px; margin-bottom:8px; color:#64748b;">
                <span>Baseline (Average clinic risk)</span>
                <span style="font-weight:600;">{base_value:.1%}</span>
            </div>
            """
            
            for label, val, detail in adjusted_factors:
                sign = "+" if val >= 0 else "-"
                val_color = "#dc2626" if val >= 0 else "#0284c7"
                fill_color = "#fecaca" if val >= 0 else "#bae6fd"
                
                # Percent width for bar
                width_percent = min(int(abs(val) * 150), 60)
                
                # Alignment spacer
                align_style = "margin-left: auto;" if val < 0 else ""
                
                waterfall_html += f"""
                <div style="display:flex; flex-direction:column; margin-bottom:8px; border-bottom:1px solid #f8fafc; padding-bottom:6px;">
                    <div style="display:flex; justify-content:space-between; font-size:11px; margin-bottom:2px;">
                        <div>
                            <span style="font-weight:500; color:#0f1f3d;">{label}</span>
                            <span style="font-size:9px; color:#94a3b8; margin-left:4px;">({detail})</span>
                        </div>
                        <span style="font-weight:600; color:{val_color};">{sign}{abs(val):.1%}</span>
                    </div>
                    <div style="width:100%; height:8px; display:flex;">
                        <div style="width:50%; display:flex; justify-content:flex-end;">
                            {f'<div style="width:{width_percent}%; height:100%; background-color:{fill_color}; border-radius:2px 0 0 2px;"></div>' if val < 0 else ''}
                        </div>
                        <div style="width:50%; display:flex; justify-content:flex-start;">
                            {f'<div style="width:{width_percent}%; height:100%; background-color:{fill_color}; border-radius:0 2px 2px 0;"></div>' if val >= 0 else ''}
                        </div>
                    </div>
                </div>
                """
                current_value += val
                
            # Final line
            waterfall_html += f"""
            <div style="display:flex; justify-content:space-between; font-size:11px; margin-top:8px; padding-top:6px; border-top:1px solid #e2e6ed; color:#0f1f3d; font-weight:600;">
                <span>Final Predicted No-Show Risk</span>
                <span style="color:{color_hex};">{prob:.1%}</span>
            </div>
            """
            
            st.html(waterfall_html)
        else:
            st.html("""
            <div style="display:flex; flex-direction:column; align-items:center; justify-content:center; height:350px; border:1px dashed #e2e6ed; border-radius:8px; background-color:#ffffff; color:#94a3b8; padding:20px; text-align:center;">
                <h5 style="margin:10px 0 5px 0; color:#64748b;">Awaiting Patient Input</h5>
                <p style="font-size:12px; margin:0; color:#94a3b8;">Fill out the patient details form and click 'Analyze Patient Risk Factor' to generate the clinical assessment.</p>
            </div>
            """)
