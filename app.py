# app.py
import datetime
import joblib
import numpy as np
import pandas as pd
import streamlit as st

# ----------------------
# Config
# ----------------------
MODEL_PATH = "models/crowd_rf_model.pkl"

# Maharashtra 2026 holidays (same set as generator) [web:10]
MAH_HOLIDAYS_2026 = {
    datetime.date(2026, 1, 26),
    datetime.date(2026, 3, 19),
    datetime.date(2026, 3, 21),
}

FESTIVAL_DATES = {
    datetime.date(2025, 9, 7),
    datetime.date(2025, 9, 8),
    datetime.date(2025, 9, 9),
    datetime.date(2025, 10, 29),
    datetime.date(2025, 10, 30),
    datetime.date(2025, 7, 10),
    datetime.date(2025, 7, 11),
}

TIME_SLOTS = [6, 7, 8, 9, 12, 13, 14, 17, 18, 19]

def is_holiday(date_obj):
    return 1 if date_obj in MAH_HOLIDAYS_2026 else 0

def is_festival(date_obj):
    return 1 if date_obj in FESTIVAL_DATES else 0

def load_model():
    return joblib.load(MODEL_PATH)

def crowd_to_marathi(label):
    if label == "High":
        return "जास्त"
    elif label == "Medium":
        return "मध्यम"
    else:
        return "कमी"

def main():
    st.set_page_config(page_title="MSRTC Crowd Predictor", layout="centered")

    st.title("🚌 MSRTC Solapur Route Crowd Predictor")
    st.write("**गर्दीचा अंदाज / Crowd Prediction for MSRTC routes**")

    model = load_model()

    # Sidebar: info
    st.sidebar.header("Project Info")
    st.sidebar.markdown(
        """
        **Mini Project**: Bus Route Crowd Predictor for MSRTC  
        - Routes around **Solapur**  
        - Uses **Random Forest** classification  
        - Considers **festival & holiday factors**
        """
    )

    # Inputs
    st.subheader("1. Select Route and Time")

    routes = [
        "Solapur-Pune",
        "Solapur-Kolhapur",
        "Solapur-Akkalkot",
        "Solapur-Pandharpur",
        "Solapur-Latur",
        "Solapur-Sangli",
    ]

    route = st.selectbox("Route", routes)

    today = datetime.date.today()
    date_input = st.date_input(
        "Date", value=today, min_value=datetime.date(2025, 4, 1), max_value=datetime.date(2026, 3, 31)
    )

    hour = st.selectbox(
        "Departure hour (24‑hour)", TIME_SLOTS, index=TIME_SLOTS.index(8)
    )

    weather = st.selectbox("Weather", ["Clear", "Cloudy", "Rain", "Heavy Rain"])

    # Prepare features
    day_of_week = date_input.weekday()
    weekend = 1 if day_of_week >= 5 else 0
    holiday_flag = is_holiday(date_input)
    festival_flag = is_festival(date_input)

    # Distance and stops mapping (same as generator)
    route_info = {
        "Solapur-Pune": (260, 10),
        "Solapur-Kolhapur": (230, 9),
        "Solapur-Akkalkot": (40, 5),
        "Solapur-Pandharpur": (70, 6),
        "Solapur-Latur": (110, 7),
        "Solapur-Sangli": (210, 8),
    }
    distance_km, num_stops = route_info[route]

    input_df = pd.DataFrame(
        [
            {
                "route": route,
                "day_of_week": day_of_week,
                "hour": hour,
                "is_weekend": weekend,
                "is_holiday": holiday_flag,
                "is_festival": festival_flag,
                "distance_km": distance_km,
                "num_stops": num_stops,
                "weather": weather,
            }
        ]
    )

    st.subheader("2. Prediction")

    if st.button("Predict Crowd"):
        pred = model.predict(input_df)[0]
        probs = model.predict_proba(input_df)[0]
        classes = model.classes_
        prob_map = dict(zip(classes, probs))
        confidence = prob_map.get(pred, 0) * 100

        marathi_label = crowd_to_marathi(pred)

        st.success(
            f"**Predicted crowd level:** {pred}  "
            f"(**गर्दीचा अंदाज:** {marathi_label})  "
            f"— Confidence: ~{confidence:.1f}%"
        )

        # Simple explanation
        reason_parts = []
        if weekend:
            reason_parts.append("weekend")
        if holiday_flag:
            reason_parts.append("Maharashtra holiday")
        if festival_flag:
            reason_parts.append("festival season")
        if "Pandharpur" in route or "Akkalkot" in route:
            reason_parts.append("pilgrimage route")

        if reason_parts:
            st.info(
                "Reasoning hint: Model is influenced by **{}**, "
                "along with hour and route.".format(", ".join(reason_parts))
            )
        else:
            st.info(
                "Reasoning hint: Model mainly considers **hour, route, and weekday pattern**."
            )

        # Extra: crowd across the day for same route & date
        st.subheader("3. Crowd across the day (same route & date)")
        rows = []
        for h in TIME_SLOTS:
            row_df = input_df.copy()
            row_df["hour"] = h
            p = model.predict(row_df)[0]
            rows.append({"hour": h, "predicted_crowd": p})
        chart_df = pd.DataFrame(rows)

        # Map label to order for plotting
        level_order = {"Low": 0, "Medium": 1, "High": 2}
        chart_df["level_num"] = chart_df["predicted_crowd"].map(level_order)

        st.bar_chart(
            chart_df.set_index("hour")["level_num"],
            height=300,
        )
        st.caption(
            "0 = Low, 1 = Medium, 2 = High. "
            "This shows how crowded the route is across different time slots."
        )

    st.markdown("---")
    st.markdown(
        "**Future Scope:** Connect with live MSRTC GPS & ticketing API to use real passenger counts."
    )

if __name__ == "__main__":
    main()
