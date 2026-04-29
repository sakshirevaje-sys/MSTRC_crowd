import streamlit as st
import pandas as pd
import joblib
import os

from datetime import datetime

from calendar_utils import get_calendar_features
from timetable_utils import load_timetable, get_next_bus

# ── Load Model ─────────────────────────────
MODEL_PATH = os.path.join("models", "crowd_rf_model.pkl")

if not os.path.exists(MODEL_PATH):
    st.error("❌ Model not found. Run train_model.py first.")
    st.stop()

model = joblib.load(MODEL_PATH)

# ── Load Timetable ─────────────────────────
timetable_df = load_timetable()

# ── Route Info ─────────────────────────────
ROUTE_INFO = {
    "Solapur-Pune": {"distance_km": 260, "num_stops": 10},
    "Solapur-Kolhapur": {"distance_km": 230, "num_stops": 9},
    "Solapur-Akkalkot": {"distance_km": 40, "num_stops": 5},
    "Solapur-Pandharpur": {"distance_km":  70, "num_stops": 6},
    "Solapur-Latur":      {"distance_km": 110, "num_stops": 7},
    "Solapur-Sangli":     {"distance_km": 210, "num_stops": 8}
}



# ── Marathi Mapping ────────────────────────
marathi_crowd = {
    "Low": "कमी",
    "Medium": "मध्यम",
    "High": "जास्त"
}

# ── UI ─────────────────────────────────────
st.set_page_config(page_title="MSRTC Crowd Predictor", layout="centered")

st.title("🚌 MSRTC Smart Crowd Predictor")
st.write("Predict crowd and get next bus suggestion")

st.write(f"🕒 Current Time: {datetime.now().strftime('%H:%M')}")

route = st.selectbox("Select Route", list(ROUTE_INFO.keys()))
date = st.date_input("Select Date")

# ✅ 24-hour time input
selected_time = st.time_input("Select Time", value=datetime.now().time())
hour = selected_time.hour

weather = st.selectbox("Weather", ["Clear", "Cloudy", "Rain"])

# ── Calendar Features ──────────────────────
calendar = get_calendar_features(date)

# ── Show Calendar Info ─────────────────────
st.markdown("### 📅 Day Information")

if calendar["is_weekend"]:
    st.info("🛑 Weekend (शनिवार/रविवार)")

if calendar["is_holiday"]:
    st.warning(f"🎉 Holiday: {calendar['holiday_name']} (सुट्टी)")

if calendar["is_festival"]:
    st.success(f"🪔 Festival: {calendar['festival_name']} (सण)")

if not (calendar["is_weekend"] or calendar["is_holiday"] or calendar["is_festival"]):
    st.write("📌 Normal Working Day (सामान्य दिवस)")

# ── Route Features ─────────────────────────
distance_km = ROUTE_INFO[route]["distance_km"]
num_stops = ROUTE_INFO[route]["num_stops"]

# ── Crowd Reason Function ──────────────────
def get_crowd_reason(prediction, hour, calendar, weather):
    reasons = []

    if hour in [7, 8, 9, 17, 18, 19]:
        reasons.append("(Peak Hours)")

    if calendar["is_weekend"]:
        reasons.append("शनिवार/रविवार गर्दी")

    if calendar["is_holiday"]:
        reasons.append(f"सार्वजनिक सुट्टी ({calendar['holiday_name']})")

    if calendar["is_festival"]:
        reasons.append(f"सण ({calendar['festival_name']})")

    if weather == "Rain":
        reasons.append("पावसामुळे गर्दी वाढते")

    if prediction == "Low":
        if hour in [12, 13, 14]:
            reasons.append("दुपारची कमी गर्दी")
        if not reasons:
            reasons.append("सामान्य परिस्थिती")

    return reasons

# ── Predict Button ─────────────────────────
if st.button("🔍 Predict Crowd"):

    input_df = pd.DataFrame([{
        "route": route,
        "day_of_week": date.weekday(),
        "hour": hour,
        "is_weekend": calendar["is_weekend"],
        "is_holiday": calendar["is_holiday"],
        "is_festival": calendar["is_festival"],
        "distance_km": distance_km,
        "num_stops": num_stops,
        "weather": weather,
    }])

    prediction = model.predict(input_df)[0]

    # Reasons
    reasons = get_crowd_reason(prediction, hour, calendar, weather)

    # Next Bus
    selected_time_str = selected_time.strftime("%H:%M")
    next_bus = get_next_bus(route, selected_time_str, timetable_df)

    # ── Output ─────────────────────────────
    st.subheader(f"🚦 Crowd Level: {prediction} ({marathi_crowd[prediction]})")

    # Special Day Impact
    st.markdown("### 🎯 विशेष दिवस प्रभाव")

    if calendar["is_festival"]:
        st.success(f"🪔 सण: {calendar['festival_name']}")

    if calendar["is_holiday"]:
        st.warning(f"🎉 सुट्टी: {calendar['holiday_name']}")

    if calendar["is_weekend"]:
        st.info("🛑 शनिवार/रविवार")

    # Crowd Message
    if prediction == "High":
        if next_bus:
            st.warning(f"⚠️ जास्त गर्दी! पुढील बस {next_bus} वाजता घ्या")
        else:
            st.warning("⚠️ जास्त गर्दी आणि पुढील बस उपलब्ध नाही")

    elif prediction == "Medium":
        st.info("ℹ️ मध्यम गर्दी. थोडं लवकर या")

    else:
        st.success("✅ कमी गर्दी. आरामदायी प्रवास")

    # Reasons
    st.markdown("### 📊 गर्दीचे कारण")
    for r in reasons:
        st.write(f"• {r}")

    # Next Bus Info
    if next_bus:
        st.success(f"🚌 पुढील बस: {next_bus}")
    else:
        st.error("❌ पुढील बस उपलब्ध नाही")