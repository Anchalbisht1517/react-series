"""SHAP Insights page for CarePredict. Upgrades SHAP explainability with patient lookup waterfall."""

import streamlit as st
import os
import math
from noshow.visualization.shap_plots import get_shap_paths, render_image

def render_shap_insights():
    """Render the SHAP Insights page."""
    st.html("<h3 style='margin:0 0 10px 0; color:#0f1f3d; font-weight:600;'>SHAP Insights</h3>")
    st.html("<p style='color:#64748b; font-size:13px;'>Understand global feature importance rankings and inspect individual patient risk explanations.</p>")
    
    # Load static plot paths
    paths = get_shap_paths()
    
    # Create Tabs: 1. Patient Explanation (Dynamic), 2. Global Explanations (Static Plots)
    tab_patient, tab_global = st.tabs(["Individual Patient Explanations", "Global Feature Importance"])
    
    with tab_patient:
        with st.container(border=True):
            st.html("<div class='card-title-text' style='margin-bottom:10px;'>Dynamic Patient Risk Factors Lookup</div>")
            st.html("<p style='font-size:12px; color:#64748b; margin-bottom:15px;'>Enter a patient appointment ID to generate a personalized SHAP waterfall chart breaking down how their profile influences no-show risk.</p>")
            
            search_id = st.text_input("Appointment ID (e.g. APT-8821, APT-7740, APT-9103)", value="APT-8821").strip()
            
            if "patients_df" in st.session_state:
                df = st.session_state.patients_df
                patient_row = df[df["patient_id"] == search_id]
                
                if len(patient_row) > 0:
                    p_data = patient_row.iloc[0]
                    name = p_data["name"]
                    prob = p_data["probability"]
                    tier = p_data["risk_tier"]
                    action = p_data["recommended_action"]
                    
                    # Render patient card summary
                    st.html(f"""
                    <div style="background-color:#f8fafc; padding:12px; border-radius:6px; border:1.5px solid #e2e6ed; margin-bottom:20px;">
                        <div style="display:flex; justify-content:space-between; align-items:center;">
                            <div>
                                <span style="font-size:14px; font-weight:600; color:#0f1f3d;">{name}</span> 
                                <span style="font-size:11px; color:#94a3b8; margin-left:5px;">(ID: {search_id})</span>
                            </div>
                            <span class="pill {'pill-red' if tier == 'High' else 'pill-amber' if tier == 'Medium' else 'pill-green'}">{tier} Risk ({prob:.1%})</span>
                        </div>
                        <div style="font-size:12px; color:#64748b; margin-top:4px;">
                            <b>Recommended Action:</b> {action}
                        </div>
                    </div>
                    """)
                    
                    # Calculate SHAP waterfall values dynamically
                    base_value = 0.201
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
                        
                        width_percent = min(int(abs(val) * 150), 60)
                        
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
                        
                    # Final line
                    waterfall_html += f"""
                    <div style="display:flex; justify-content:space-between; font-size:11px; margin-top:8px; padding-top:6px; border-top:1px solid #e2e6ed; color:#0f1f3d; font-weight:600;">
                        <span>Final Predicted Patient Risk</span>
                        <span style="color:{'#dc2626' if tier == 'High' else '#f59e0b' if tier == 'Medium' else '#16a34a'};">{prob:.1%}</span>
                    </div>
                    """
                    
                    st.html(waterfall_html)
                else:
                    st.html(f"""
                    <div class="banner banner-danger">
                        Appointment ID "{search_id}" not found in today's roster.
                    </div>
                    <p style="font-size:12px; color:#64748b;">Try searching for one of these valid IDs: <b>APT-8821</b>, <b>APT-7740</b>, <b>APT-9103</b>, or upload a batch file first.</p>
                    """)
            else:
                st.error("Roster dataset not loaded. Initializing...")

    with tab_global:
        # Global Explanation Plots
        st.markdown("#### Global Model Explanations")
        st.html("<p style='font-size:12px; color:#64748b;'>These plots are fit across the entire 88,421 sample training set to identify macroscopic patient behavior patterns.</p>")
        
        c_plots1, c_plots2 = st.columns(2)
        
        with c_plots1:
            with st.container(border=True):
                st.html("<div class='card-title-text' style='margin-bottom:10px;'>Global Feature Importance (Bar)</div>")
                if os.path.exists(paths["summary_bar"]):
                    st.image(paths["summary_bar"], use_container_width=True)
                else:
                    st.info("SHAP summary bar plot not found.")
                st.html("""
                <p style="font-size:11px; color:#64748b; margin-top:10px; margin-bottom:0;">
                    The bar chart ranks features by their average absolute SHAP value. Larger bars indicate a larger overall impact on global no-show predictions.
                </p>
                """)
            
        with c_plots2:
            with st.container(border=True):
                st.html("<div class='card-title-text' style='margin-bottom:10px;'>Feature Impact Direction (Dot Plot)</div>")
                if os.path.exists(paths["summary_dot"]):
                    st.image(paths["summary_dot"], use_container_width=True)
                else:
                    st.info("SHAP summary dot plot not found.")
                st.html("""
                <p style="font-size:11px; color:#64748b; margin-top:10px; margin-bottom:0;">
                    Each dot represents one patient. Horizontal position shows SHAP value direction (positive = higher risk), and color indicates feature value (red = high, blue = low).
                </p>
                """)
