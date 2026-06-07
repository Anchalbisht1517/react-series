"""Reports page for CarePredict. Displays downloadable operational reports."""

import streamlit as st
import pandas as pd

def render_reports():
    """Render the Reports page."""
    st.html("<h3 style='margin:0 0 10px 0; color:#0f1f3d; font-weight:600;'>Reports</h3>")
    st.html("<p style='color:#64748b; font-size:13px;'>Compile and download medical operational and compliance reports for hospital administration.</p>")
    
    st.html("""
    <div class="card card-sky-blue" style="padding:20px; margin-bottom:20px;">
        <div class="card-title-text" style="margin-bottom:12px;">Available Report Compilation Library</div>
        <p style="font-size:12px; color:#64748b; margin-top:-10px;">Select a report from our hospital audit library below to generate a print-ready spreadsheet or document.</p>
        
        <!-- Report 1 -->
        <div style="display:flex; justify-content:space-between; align-items:center; padding:12px 0; border-bottom:1px solid #f1f5f9;">
            <div>
                <span style="font-size:13px; font-weight:600; color:#0f1f3d;">No-Show Operational Audit Report</span>
                <div style="font-size:11px; color:#94a3b8;">Detailed analysis of appointment no-show frequency, cost audits, and clinic-by-clinic risk stats.</div>
            </div>
            <button class="action-badge action-standard" style="cursor:pointer; padding:6px 12px; background-color:#ffffff; font-weight:500;">Generate PDF</button>
        </div>
        
        <!-- Report 2 -->
        <div style="display:flex; justify-content:space-between; align-items:center; padding:12px 0; border-bottom:1px solid #f1f5f9;">
            <div>
                <span style="font-size:13px; font-weight:600; color:#0f1f3d;">Clinician Outreach Activity Sheet</span>
                <div style="font-size:11px; color:#94a3b8;">Logs coordinator call and SMS activities, audit trail compliance, and intervention success feedback loop.</div>
            </div>
            <button class="action-badge action-standard" style="cursor:pointer; padding:6px 12px; background-color:#ffffff; font-weight:500;">Export CSV</button>
        </div>
        
        <!-- Report 3 -->
        <div style="display:flex; justify-content:space-between; align-items:center; padding:12px 0;">
            <div>
                <span style="font-size:13px; font-weight:600; color:#0f1f3d;">Model Recalibration & Validation Sheet</span>
                <div style="font-size:11px; color:#94a3b8;">Drift statistics, validation metrics over the past 30 days, and SMOTE resampling audit metrics.</div>
            </div>
            <button class="action-badge action-standard" style="cursor:pointer; padding:6px 12px; background-color:#ffffff; font-weight:500;">Generate PDF</button>
        </div>
    </div>
    """)
    
    st.info("Reporting functions are running in audit trial mode. Contact hospital system administrator for Epic/Cerner API export sync.")
