"""Streamlit page: 2_Single_Patient_Check

Input form for a single patient, run prediction pipeline, show risk tier.
Build this page first — it validates the entire end-to-end pipeline.
"""

import os
import sys
import streamlit as st

# Ensure src is discoverable
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
src_path = os.path.join(project_root, "src")
if src_path not in sys.path:
    sys.path.insert(0, src_path)

from noshow.pipeline.prediction_pipeline import PredictionPipeline
from noshow.exception import NoShowException

st.set_page_config(page_title="Single Patient Check", page_icon="🧑‍⚕️")

st.title("🧑‍⚕️ Single Patient Check")

st.markdown("""
Enter patient details below to predict the no-show probability and receive a
recommended action.
""")

# ------------------------------------------------------------------
# Input form
# ------------------------------------------------------------------
with st.form("patient_form"):
    st.subheader("Patient Information")

    age = st.number_input("Age", min_value=0, max_value=110, value=30, step=1)
    gender = st.selectbox("Gender", options=["Female", "Male"])
    neighbourhood = st.text_input("Neighbourhood", value="JARDIM DA PENHA")

    col1, col2 = st.columns(2)
    with col1:
        scholarship = st.selectbox("Scholarship", options=[0, 1], format_func=lambda x: "Yes" if x == 1 else "No")
        hypertension = st.selectbox("Hypertension", options=[0, 1], format_func=lambda x: "Yes" if x == 1 else "No")
        diabetes = st.selectbox("Diabetes", options=[0, 1], format_func=lambda x: "Yes" if x == 1 else "No")
    with col2:
        alcoholism = st.selectbox("Alcoholism", options=[0, 1], format_func=lambda x: "Yes" if x == 1 else "No")
        handicap = st.selectbox("Handicap Level", options=[0, 1, 2, 3, 4])
        sms_received = st.selectbox("SMS Received", options=[0, 1], format_func=lambda x: "Yes" if x == 1 else "No")

    days_waiting = st.number_input("Days Waiting", min_value=0, max_value=365, value=5, step=1)
    appointment_weekday = st.selectbox(
        "Appointment Weekday",
        options=[0, 1, 2, 3, 4, 5, 6],
        format_func=lambda x: ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"][x],
    )
    previous_no_shows = st.number_input("Previous No-Shows", min_value=0, max_value=100, value=0, step=1)

    submitted = st.form_submit_button("Predict No-Show Risk")

# ------------------------------------------------------------------
# Prediction
# ------------------------------------------------------------------
if submitted:
    patient = {
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
        with st.spinner("Running prediction pipeline..."):
            pipeline = PredictionPipeline()
            result = pipeline.predict(patient)

        prob = result["probability"]
        tier = result["tier"]
        action = result["action"]

        st.markdown("---")
        st.subheader("Prediction Result")

        if tier == "High":
            st.error(f"🔴 **High Risk** — Probability: `{prob:.2%}`")
        elif tier == "Medium":
            st.warning(f"🟡 **Medium Risk** — Probability: `{prob:.2%}`")
        else:
            st.success(f"🟢 **Low Risk** — Probability: `{prob:.2%}`")

        st.markdown(f"**Recommended Action:** {action}")

        # Probability gauge
        st.progress(min(int(prob * 100), 100))

    except NoShowException as e:
        st.error(f"Prediction pipeline error: {e}")
        st.info("Ensure the data pipeline and model trainer have been run first.")
    except Exception as e:
        st.error(f"Unexpected error: {e}")
