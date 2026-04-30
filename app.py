import streamlit as st
from datetime import date
import time as t
import random

# =========================
# Page config
# =========================
st.set_page_config(
    page_title="MSRTC Smart Crowd Predictor",
    page_icon="🚍",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# =========================
# CSS: better label visibility + strong contrast
# =========================
st.markdown(
    """
<style>
.stApp{
  background:
    radial-gradient(900px circle at 15% 10%, rgba(124,58,237,0.32), transparent 55%),
    radial-gradient(800px circle at 80% 25%, rgba(31,119,180,0.22), transparent 55%),
    radial-gradient(900px circle at 30% 85%, rgba(34,197,94,0.14), transparent 60%),
    linear-gradient(180deg,#070A12 0%, #060814 50%, #050611 100%);
  color: #FFFFFF;
}
.block-container{ padding-top: 1.2rem; padding-bottom: 2.5rem; }

#MainMenu {visibility:hidden;}
footer {visibility:hidden;}
header {visibility:hidden;}

.card{
  background: rgba(255,255,255,0.06);
  border: 1px solid rgba(255,255,255,0.12);
  box-shadow: 0 18px 50px rgba(0,0,0,0.45);
  border-radius: 18px;
  padding: 18px 18px;
  backdrop-filter: blur(12px);
  -webkit-backdrop-filter: blur(12px);
}

.h-title{
  font-size: 2.05rem;
  font-weight: 950;
  margin: 0;
  line-height: 1.15;
  background: linear-gradient(90deg, #A78BFA, #60A5FA, #34D399);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}
.h-sub{
  margin-top: 6px;
  color: rgba(255,255,255,0.80);
  font-size: 1.02rem;
}

.section-title{
  font-size: 1.05rem;
  letter-spacing: 0.3px;
  font-weight: 850;
  color: rgba(255,255,255,0.92);
  margin-bottom: 10px;
}

.hr{
  height:1px;
  background: linear-gradient(90deg, transparent, rgba(255,255,255,0.20), transparent);
  border: 0;
  margin: 14px 0;
}

/* IMPORTANT: Make labels strong + colored (fix "not showing labels") */
div[data-testid="stWidgetLabel"] > label,
label, .stSelectbox label, .stDateInput label, .stTextInput label {
  color: #E9D5FF !important;    /* soft purple */
  font-weight: 800 !important;
  font-size: 0.95rem !important;
  letter-spacing: 0.2px !important;
}

/* Help text */
small, .stCaption, .stMarkdown small { color: rgba(255,255,255,0.75) !important; }

/* Result box: blue background + WHITE text */
.result-box {
    background: linear-gradient(135deg, #1f77b4, #155a86);
    color: #FFFFFF;
    padding: 16px;
    border-radius: 14px;
    font-size: 18px;
    border: 1px solid rgba(255,255,255,0.16);
    box-shadow: 0 18px 45px rgba(0,0,0,0.38);
}

/* Festival box: special highlight */
.festival-box {
    background: linear-gradient(135deg, rgba(250,204,21,0.18), rgba(249,115,22,0.14));
    color: #FFFFFF;
    padding: 14px;
    border-radius: 14px;
    border: 1px solid rgba(250,204,21,0.35);
    box-shadow: 0 16px 40px rgba(0,0,0,0.35);
}

/* Badges */
.badge{
  display:inline-flex;
  align-items:center;
  gap:10px;
  padding: 8px 12px;
  border-radius: 999px;
  border: 1px solid rgba(255,255,255,0.14);
  background: rgba(255,255,255,0.06);
  color: #FFFFFF;
  font-weight: 850;
  font-size: 0.92rem;
}

/* Button */
div.stButton > button{
  width: 100%;
  border-radius: 14px;
  border: 1px solid rgba(255,255,255,0.14);
  background: linear-gradient(135deg, rgba(124,58,237,0.85), rgba(14,165,233,0.65));
  color: #FFFFFF;
  padding: 0.92rem 1rem;
  font-weight: 950;
  transition: transform 140ms ease, box-shadow 140ms ease, filter 140ms ease;
  box-shadow: 0 18px 46px rgba(0,0,0,0.42);
}
div.stButton > button:hover{
  transform: translateY(-1px) scale(1.01);
  filter: brightness(1.06);
  box-shadow: 0 22px 56px rgba(0,0,0,0.55);
}
</style>
""",
    unsafe_allow_html=True,
)

# =========================
# Header
# =========================
st.markdown(
    """
<div class="card">
  <div style="display:flex; align-items:center; justify-content:space-between; gap:14px;">
    <div>
      <div class="h-title">🚍 MSRTC Smart Crowd Predictor</div>
      <div class="h-sub">AM/PM time • Clear labels • Travel-type messages • Festival output</div>
    </div>
    <div style="font-size:3.1rem; opacity:0.92;">🚌</div>
  </div>
</div>
""",
    unsafe_allow_html=True,
)
st.write("")

# =========================
# Fixed Source + destination list
# =========================
source = "Solapur"
destinations = [
    "Pune", "Kolhapur", "Akkalkot", "Pandharpur",
    "Dharashiv", "Latur", "Mumbai", "Tuljapur",
    "Sangola", "Barshi", "Swargate"
]

# =========================
# Time: generated 24 hours, displayed AM/PM
# =========================
def hour_to_ampm_label(h: int) -> str:
    if h == 0:
        return "12 AM"
    if 1 <= h <= 11:
        return f"{h} AM"
    if h == 12:
        return "12 PM"
    return f"{h-12} PM"

# You still get full-day usability; just shown as AM/PM
time_slots = [hour_to_ampm_label(h) for h in range(24)]
label_to_hour = {hour_to_ampm_label(h): h for h in range(24)}

# =========================
# Festival detection (customize)
# =========================
festival_dates = {
    "2026-11-12": "Diwali",
    "2026-03-08": "Holi",
    "2026-08-15": "Independence Day",
    "2026-10-02": "Gandhi Jayanti",
}
def check_festival(d: date):
    return festival_dates.get(d.strftime("%Y-%m-%d"), None)

# =========================
# Required crowd logic
# =========================
def crowd_level_logic(occupancy: int) -> str:
    if occupancy > 75:
        return "High"
    elif occupancy > 40:
        return "Medium"
    else:
        return "Low"

marathi_map = {
    "High": "जास्त गर्दी अपेक्षित आहे. पुढील वेळ निवडा.",
    "Medium": "मध्यम गर्दी. थोडे लवकर जा.",
    "Low": "कमी गर्दी. आरामदायक प्रवास."
}
def suggestion_bilingual(level: str):
    if level == "High":
        eng = "High crowd expected. Try next time slot."
    elif level == "Medium":
        eng = "Moderate crowd. Travel a bit early."
    else:
        eng = "Low crowd. Comfortable journey."
    return eng, marathi_map[level]

# =========================
# Travel type messaging (more effective idea)
# =========================
def get_travel_message(level: str, travel_type: str, hour: int) -> str:
    """
    More effective than generic text:
    - adds practical action (arrive early / avoid peak / keep buffer)
    - ties to time + purpose
    """
    peak = (8 <= hour <= 10) or (18 <= hour <= 20)

    if travel_type == "Student":
        # Student: class timing + seat preference + punctuality
        if level == "High":
            return "🎒 Student tip: College rush time. Leave 30–45 min early or choose the next slot."
        if level == "Medium":
            return "🎒 Student tip: Manageable crowd. Reach stand 10–15 min early for a seat."
        return "🎒 Student tip: Best slot for comfortable travel—good chance of seating."

    if travel_type == "Office Worker":
        # Office worker: peak hours + buffer time
        if level == "High":
            return "💼 Office tip: Peak commute. Add 20–30 min buffer or travel after peak hours."
        if level == "Medium":
            return "💼 Office tip: Moderate rush. Keep buffer time and board early."
        return "💼 Office tip: Smooth commute expected—good time to travel."

    # Tourist
    if level == "High":
        return "🧳 Tourist tip: Avoid peak crowd—travel mid-day for comfort and easier luggage handling."
    if level == "Medium":
        return "🧳 Tourist tip: Some crowd expected—keep essentials handy and arrive early."
    return "🧳 Tourist tip: Relaxed slot—ideal for sightseeing travel."

# =========================
# Festival-specific output (different output)
# =========================
def festival_output(festival: str | None, level: str) -> tuple[str, int]:
    """
    Returns:
      festival_msg (special message),
      festival_boost (occupancy increase)
    """
    if not festival:
        return ("", 0)

    # Different festival outputs depending on level
    if level == "High":
        msg = f"🎉 Festival Active: {festival} → Expect heavy rush. Prefer earlier or later buses."
    elif level == "Medium":
        msg = f"🎉 Festival Active: {festival} → Crowd may rise quickly. Try to book/arrive early."
    else:
        msg = f"🎉 Festival Active: {festival} → Currently low, but rush can increase suddenly."
    return (msg, 10)

# =========================
# Best-time engine (+/- 1 hour)
# =========================
def simulate_base_occupancy(dest: str, day_name: str, hour: int) -> int:
    occ = 35
    # rush hours
    if hour in [8, 9, 10, 18, 19, 20]:
        occ += 30
    # weekend
    if day_name in ["Saturday", "Sunday"]:
        occ += 15
    # Mumbai factor
    if dest == "Mumbai":
        occ += 10
    # randomness
    occ += random.randint(-6, 10)
    return max(5, min(98, occ))

def apply_travel_type_weight(occ: int, travel_type: str) -> int:
    # small, realistic personalization
    if travel_type == "Office Worker":
        occ += 6
    elif travel_type == "Tourist":
        occ += 3
    return max(5, min(98, occ))

def suggest_best_time(dest: str, day_name: str, hour: int, festival_on: bool, travel_type: str):
    candidates = [max(0, hour - 1), hour, min(23, hour + 1)]
    best_h, best_occ = hour, 999
    for h in candidates:
        occ = simulate_base_occupancy(dest, day_name, h)
        if festival_on:
            occ = min(98, occ + 8)  # festival pushes crowd overall
        occ = apply_travel_type_weight(occ, travel_type)
        if occ < best_occ:
            best_occ = occ
            best_h = h
    return hour_to_ampm_label(best_h), int(best_occ)

# =========================
# UI Layout
# =========================
left, right = st.columns([1.05, 1.25], gap="large")

with left:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">🧾 Input</div>', unsafe_allow_html=True)

    st.text_input("🚍 Source (Fixed)", value=source, disabled=True)

    destination = st.selectbox("🏁 Select Destination", destinations)

    col1, col2 = st.columns(2)
    with col1:
        travel_date = st.date_input("📅 Select Date", value=date.today())
    with col2:
        selected_time_label = st.selectbox("⏰ Select Time (AM/PM)", time_slots, index=8)  # 8 AM default

    travel_type = st.selectbox("🧍 Travel Type", ["Student", "Office Worker", "Tourist"], index=0)

    st.markdown("<hr class='hr'/>", unsafe_allow_html=True)
    st.markdown("<div style='text-align:center'>", unsafe_allow_html=True)
    predict = st.button("🔍 Predict Crowd")
    st.markdown("</div>", unsafe_allow_html=True)

    st.caption("Labels are intentionally bright for visibility. Output uses high contrast.")
    st.markdown("</div>", unsafe_allow_html=True)

with right:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">📊 Result</div>', unsafe_allow_html=True)
    st.write("Click **Predict Crowd** to view output with AM/PM time, travel-type message, and festival special output.")
    st.markdown("</div>", unsafe_allow_html=True)

# =========================
# Prediction
# =========================
if predict:
    hour = label_to_hour[selected_time_label]
    day_name = travel_date.strftime("%A")
    festival = check_festival(travel_date)
    festival_on = festival is not None

    with st.spinner("⏳ Predicting crowd..."):
        t.sleep(0.9)

    # Base occupancy
    occupancy = simulate_base_occupancy(destination, day_name, hour)

    # Travel type personalization
    occupancy = apply_travel_type_weight(occupancy, travel_type)

    # Level first, then festival message + boost
    level = crowd_level_logic(occupancy)
    fest_msg, fest_boost = festival_output(festival, level)
    if festival_on:
        occupancy = min(98, occupancy + fest_boost)

    # Recompute level after festival boost (more realistic)
    level = crowd_level_logic(occupancy)

    eng_msg, mar_msg = suggestion_bilingual(level)
    travel_msg = get_travel_message(level, travel_type, hour)

    best_time, best_occ = suggest_best_time(destination, day_name, hour, festival_on, travel_type)

    # Peak hour line
    peak_msg = "Peak hour detected (office rush)" if ((8 <= hour <= 10) or (18 <= hour <= 20)) else "Normal/Off-peak"

    # Badge colors (visual)
    level_badge = {"High": "🔴 High", "Medium": "🟡 Medium", "Low": "🟢 Low"}[level]

    with right:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown('<div class="section-title">✅ Final Output</div>', unsafe_allow_html=True)

        # Progress bar (important)
        st.markdown("**📊 Occupancy Progress**")
        st.progress(occupancy / 100)

        # Festival special area (different output)
        if festival_on:
            st.markdown(
                f"""
                <div class="festival-box">
                  <span class="badge">🎉 Festival Active</span>
                  <div style="margin-top:10px; font-weight:850; font-size:1.05rem;">
                    {fest_msg}
                  </div>
                </div>
                """,
                unsafe_allow_html=True,
            )
            st.write("")

        # Main result box (blue bg + white text)
        st.markdown(
            f"""
<div class="result-box">
🚍 <b>Source:</b> {source} <br>
🏁 <b>Destination:</b> {destination} <br>
📅 <b>Date:</b> {travel_date.strftime("%d-%m-%Y")} ({day_name}) <br>
⏰ <b>Time:</b> {selected_time_label} <span style="opacity:0.9;">({peak_msg})</span><br><br>

🚦 <b>Crowd Level:</b> {level_badge} <br>
📊 <b>Occupancy:</b> {occupancy}% <br><br>

📢 <b>Suggestion:</b><br>
EN: {eng_msg}<br>
MR: {mar_msg}<br><br>

💡 <b>Travel Insight ({travel_type}):</b> {travel_msg}<br><br>

⏰ <b>Best Time Recommendation:</b> {best_time} (≈{best_occ}% crowd)
</div>
""",
            unsafe_allow_html=True,
        )

        # Streamlit smart alerts
        if level == "Low":
            st.success("🟢 Comfortable: Low crowd expected.")
        elif level == "Medium":
            st.warning("🟡 Moderate: Some crowd expected. Reach early.")
        else:
            st.error("🔴 Crowded: High crowd expected. Consider another time.")

        st.markdown("</div>", unsafe_allow_html=True)
