import streamlit as st
import pandas as pd
import joblib

# Page config
st.set_page_config(
    page_title="Patient No-Show Predictor",
    page_icon="🏥",
    layout="wide"
)

# Custom CSS
st.markdown("""
    <style>
    .main { background-color: #f0f4f8; }
    .block-container { padding: 2rem 3rem; }
    .stButton > button {
        background-color: #1F4E79;
        color: white;
        font-size: 18px;
        padding: 14px;
        border-radius: 10px;
        width: 100%;
        border: none;
        margin-top: 10px;
    }
    .stButton > button:hover {
        background-color: #2E75B6;
    }
    .metric-card {
        background: white;
        border-radius: 12px;
        padding: 20px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        text-align: center;
    }
    .risk-high {
        background: linear-gradient(135deg, #ff4b4b, #ff8c8c);
        color: white;
        padding: 20px;
        border-radius: 12px;
        text-align: center;
        font-size: 22px;
        font-weight: bold;
    }
    .risk-low {
        background: linear-gradient(135deg, #00c851, #00e676);
        color: white;
        padding: 20px;
        border-radius: 12px;
        text-align: center;
        font-size: 22px;
        font-weight: bold;
    }
    .section-header {
        background: #1F4E79;
        color: white;
        padding: 10px 20px;
        border-radius: 8px;
        margin-bottom: 15px;
    }
    </style>
""", unsafe_allow_html=True)

# Load model
model = joblib.load('xgboost_model_v2.pkl')

# Header
st.markdown("<h1 style='text-align:center; color:#1F4E79;'>🏥 Patient No-Show Risk Predictor</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center; color:gray; font-size:16px;'>Powered by XGBoost Machine Learning | Healthcare Decision Support Tool</p>", unsafe_allow_html=True)
st.divider()

# Stats bar
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.markdown("<div class='metric-card'><h3>110,527</h3><p>Patients Trained On</p></div>", unsafe_allow_html=True)
with col2:
    st.markdown("<div class='metric-card'><h3>83%</h3><p>No-Show Recall Rate</p></div>", unsafe_allow_html=True)
with col3:
    st.markdown("<div class='metric-card'><h3>XGBoost</h3><p>Algorithm Used</p></div>", unsafe_allow_html=True)
with col4:
    st.markdown("<div class='metric-card'><h3>15</h3><p>Features Analyzed</p></div>", unsafe_allow_html=True)

st.divider()

# Input form
st.markdown("<div class='section-header'><b>📋 Enter Patient Details</b></div>", unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("**👤 Patient Info**")
    age = st.number_input("Age", min_value=0, max_value=120, value=30)
    gender = st.selectbox("Gender", ["Female", "Male"])
    neighbourhood = st.number_input("Neighbourhood Code", min_value=0, max_value=81, value=10)
    scholarship = st.selectbox("On Welfare Program?", ["No", "Yes"])

with col2:
    st.markdown("**🏥 Medical Info**")
    hipertension = st.selectbox("Has Hypertension?", ["No", "Yes"])
    diabetes = st.selectbox("Has Diabetes?", ["No", "Yes"])
    alcoholism = st.selectbox("Has Alcoholism?", ["No", "Yes"])
    handcap = st.selectbox("Has Handicap?", ["No", "Yes"])

with col3:
    st.markdown("**📅 Appointment Info**")
    sms_received = st.selectbox("SMS Reminder Sent?", ["No", "Yes"])
    days_waiting = st.number_input("Days Between Booking & Appointment", min_value=0, max_value=365, value=7)
    appointment_weekday = st.selectbox("Appointment Day", ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"])
    scheduled_hour = st.slider("Hour Appointment Was Booked", 0, 23, 10)

st.divider()

# Predict button
if st.button("🔍 Predict No-Show Risk"):

    # Encode
    gender_val = 1 if gender == "Male" else 0
    scholarship_val = 1 if scholarship == "Yes" else 0
    hipertension_val = 1 if hipertension == "Yes" else 0
    diabetes_val = 1 if diabetes == "Yes" else 0
    alcoholism_val = 1 if alcoholism == "Yes" else 0
    handcap_val = 1 if handcap == "Yes" else 0
    sms_val = 1 if sms_received == "Yes" else 0
    weekday_val = ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday"].index(appointment_weekday)

    # Engineer
    same_day = 1 if days_waiting == 0 else 0
    if age <= 12: age_group = 0
    elif age <= 18: age_group = 1
    elif age <= 35: age_group = 2
    elif age <= 60: age_group = 3
    else: age_group = 4
    is_weekend = 1 if weekday_val >= 5 else 0
    long_wait = 1 if days_waiting > 30 else 0

    input_data = pd.DataFrame([{
        'gender': gender_val, 'age': age,
        'neighbourhood': neighbourhood,
        'scholarship': scholarship_val,
        'hipertension': hipertension_val,
        'diabetes': diabetes_val,
        'alcoholism': alcoholism_val,
        'handcap': handcap_val,
        'sms_received': sms_val,
        'days_waiting': days_waiting,
        'appointment_weekday': weekday_val,
        'scheduled_hour': scheduled_hour,
        'same_day': same_day,
        'age_group': age_group,
        'is_weekend': is_weekend,
        'long_wait': long_wait
    }])

    probability = model.predict_proba(input_data)[0][1] * 100

    # Result
    st.markdown("<div class='section-header'><b>📊 Prediction Result</b></div>", unsafe_allow_html=True)

    col1, col2 = st.columns([1, 2])

    with col1:
        if probability >= 50:
            st.markdown(f"<div class='risk-high'>🚨 HIGH RISK<br>{probability:.1f}%<br>No-Show Probability</div>", unsafe_allow_html=True)
        else:
            st.markdown(f"<div class='risk-low'>✅ LOW RISK<br>{probability:.1f}%<br>No-Show Probability</div>", unsafe_allow_html=True)

    with col2:
        st.markdown("**Risk Meter:**")
        st.progress(int(probability))

        if probability >= 50:
            st.error("📱 **Action Required:** Send SMS reminder to this patient immediately!")
            st.markdown(f"""
            **Why is this patient at risk?**
            - Age: {age} years
            - Waiting {days_waiting} days for appointment
            - SMS sent: {sms_received}
            - Appointment on: {appointment_weekday}
            """)
        else:
            st.success("✅ **No Action Needed:** Patient is likely to show up.")
            st.markdown(f"""
            **Why is this patient low risk?**
            - Age: {age} years
            - Waiting only {days_waiting} days
            - SMS sent: {sms_received}
            """)

# Footer
st.divider()
st.markdown("<p style='text-align:center; color:gray;'>Built with XGBoost + Streamlit | Patient No-Show Risk Analysis Project</p>", unsafe_allow_html=True)