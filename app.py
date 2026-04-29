import streamlit as st
from datetime import time
import time as t
import random

# ----------------------------
# Page config
# ----------------------------
st.set_page_config(
    page_title="MSRTC Crowd Predictor",
    page_icon="🚌",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# ----------------------------
# Dark + gradient + glassmorphism CSS
# ----------------------------
st.markdown(
    """
    <style>
      /* App background */
      .stApp {
        background: radial-gradient(1200px circle at 10% 10%, rgba(99,102,241,0.25), transparent 50%),
                    radial-gradient(900px circle at 90% 20%, rgba(16,185,129,0.18), transparent 55%),
                    radial-gradient(1000px circle at 30% 90%, rgba(236,72,153,0.16), transparent 55%),
                    linear-gradient(180deg, #0b1220 0%, #070b14 100%);
        color: #e5e7eb;
      }

      /* Reduce top padding a bit */
      .block-container { padding-top: 2.0rem; padding-bottom: 3rem; max-width: 780px; }

      /* Hide Streamlit footer/menu */
      #MainMenu {visibility: hidden;}
      footer {visibility: hidden;}
      header {visibility: hidden;}

      /* Glass card */
      .glass {
        background: rgba(255,255,255,0.06);
        border: 1px solid rgba(255,255,255,0.10);
        box-shadow: 0 20px 50px rgba(0,0,0,0.35);
        border-radius: 18px;
        padding: 18px 18px;
        backdrop-filter: blur(12px);
        -webkit-backdrop-filter: blur(12px);
      }

      .title {
        font-size: 2.05rem;
        font-weight: 750;
        letter-spacing: 0.2px;
        margin: 0;
        line-height: 1.2;
      }
      .subtitle {
        margin-top: 0.4rem;
        color: rgba(229,231,235,0.75);
        font-size: 1.02rem;
      }

      .chip {
        display: inline-flex;
        align-items: center;
        gap: 8px;
        padding: 8px 12px;
        border-radius: 999px;
        border: 1px solid rgba(255,255,255,0.10);
        background: rgba(255,255,255,0.05);
        color: rgba(229,231,235,0.9);
        font-size: 0.95rem;
      }

      .muted {
        color: rgba(229,231,235,0.65);
        font-size: 0.92rem;
      }

      /* Result badges */
      .badge {
        display:inline-flex;
        align-items:center;
        gap:10px;
        padding: 10px 12px;
        border-radius: 14px;
        border: 1px solid rgba(255,255,255,0.10);
        background: rgba(255,255,255,0.05);
        margin-top: 6px;
      }
      .dot {
        width: 10px;
        height: 10px;
        border-radius: 999px;
        display: inline-block;
        box-shadow: 0 0 0 4px rgba(255,255,255,0.03);
      }

      .high { color: #fecaca; }
      .med  { color: #fde68a; }
      .low  { color: #bbf7d0; }

      .dot-high { background: #ef4444; }
      .dot-med  { background: #f59e0b; }
      .dot-low  { background: #22c55e; }

      /* Progress bar container feel */
      .barwrap {
        margin-top: 10px;
        padding: 12px;
        border-radius: 16px;
        border: 1px solid rgba(255,255,255,0.10);
        background: rgba(255,255,255,0.04);
      }

      /* Button styling */
      div.stButton > button {
        width: 100%;
        border-radius: 14px;
        border: 1px solid rgba(255,255,255,0.12);
        background: linear-gradient(135deg, rgba(99,102,241,0.70), rgba(236,72,153,0.55));
        color: white;
        padding: 0.9rem 1rem;
        font-weight: 650;
        transition: transform 120ms ease, box-shadow 120ms ease, filter 120ms ease;
        box-shadow: 0 16px 40px rgba(0,0,0,0.35);
      }
      div.stButton > button:hover {
        transform: translateY(-1px) scale(1.01);
        filter: brightness(1.05);
        box-shadow: 0 18px 46px rgba(0,0,0,0.45);
      }

      /* Selectbox + input spacing */
      .stSelectbox, .stTimeInput { margin-bottom: 0.35rem; }
    </style>
    """,
    unsafe_allow_html=True,
)

# ----------------------------
# Header
# ----------------------------
st.markdown(
    """
    <div class="glass">
      <div style="display:flex; align-items:center; justify-content:space-between; gap:14px;">
        <div>
          <p class="title">MSRTC Crowd Predictor</p>
          <p class="subtitle">Plan your journey smarter</p>
          <div style="margin-top:10px;">
            <span class="chip">🚌 MSRTC • Crowd Forecast</span>
            <span class="chip">🌙 Dark • Glass UI</span>
          </div>
        </div>
        <div style="font-size:3.2rem; opacity:0.9; line-height:1;">🚌</div>
      </div>
      <div style="margin-top:10px;" class="muted">
        Tip: predictions may vary by route, day, and time. Choose carefully.
      </div>
    </div>
    """,
    unsafe_allow_html=True,
)

st.write("")

# ----------------------------
# Inputs
# ----------------------------
# Replace these with your real stops if you have a list
SOURCES = ["Solapur", "Pune", "Mumbai"]
DESTS = ["Pune", "Mumbai", "Solapur"]

DAYS = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

with st.container():
    st.markdown('<div class="glass">', unsafe_allow_html=True)
    st.subheader("Trip details")

    c1, c2 = st.columns(2)
    with c1:
        source = st.selectbox("Source", SOURCES, index=0)
    with c2:
        destination = st.selectbox("Destination", DESTS, index=1)

    c3, c4 = st.columns(2)
    with c3:
        day = st.selectbox("Day", DAYS, index=0)
    with c4:
        # Time picker: choose time of day
        journey_time = st.time_input("Time", value=time(9, 0))

    st.caption("Info: Avoid selecting the same Source & Destination.")
    predict_clicked = st.button("Predict Crowd")
    st.markdown("</div>", unsafe_allow_html=True)

# ----------------------------
# Prediction integration (stub)
# Replace this with your real model/function.
# ----------------------------
def predict_crowd(source: str, destination: str, day: str, journey_time: time):
    """
    Return: (level: 'High'|'Medium'|'Low', occupancy_percent: int, best_time_text: str|None)
    Replace this stub with your real model.
    """
    # Simple heuristic demo:
    hour = journey_time.hour
    base = 40

    if day in ["Saturday", "Sunday"]:
        base += 20
    if hour in [8, 9, 10, 18, 19, 20]:
        base += 30
    if source == "Mumbai" or destination == "Mumbai":
        base += 10

    occupancy = min(98, max(5, base + random.randint(-8, 10)))

    if occupancy >= 75:
        level = "High"
        best_time = "Try 11:00 AM – 3:00 PM for lighter crowd."
    elif occupancy >= 45:
        level = "Medium"
        best_time = "Try 10:30 AM – 12:00 PM for a slightly better chance."
    else:
        level = "Low"
        best_time = "Good time to travel — crowd is usually low."
    return level, occupancy, best_time


def marathi_line(level: str, occupancy: int):
    # Marathi digits (optional nice touch)
    trans = str.maketrans("0123456789", "०१२३४५६७८९")
    occ_mr = str(occupancy).translate(trans)

    if level == "High":
        return f"जास्त गर्दी – {occ_mr}% सीट भरलेली"
    if level == "Medium":
        return f"मध्यम गर्दी – {occ_mr}% सीट भरलेली"
    return f"कमी गर्दी – {occ_mr}% सीट भरलेली"


def level_style(level: str):
    if level == "High":
        return "high", "dot-high", "🚨"
    if level == "Medium":
        return "med", "dot-med", "⚠️"
    return "low", "dot-low", "✅"


# ----------------------------
# Output
# ----------------------------
if predict_clicked:
    if source == destination:
        st.error("Source and Destination cannot be the same.")
    else:
        # Loading animation
        with st.spinner("Predicting crowd…"):
            t.sleep(1.1)  # simulate compute time; remove for real prediction

            level, occupancy, best_time = predict_crowd(source, destination, day, journey_time)

        color_cls, dot_cls, icon = level_style(level)
        suggestion_en = {
            "High": "Consider traveling earlier/later to avoid peak rush.",
            "Medium": "You may get seats, but expect some crowd.",
            "Low": "Comfortable journey expected — good time to travel.",
        }[level]

        # Result card (fade-ish effect: Streamlit renders instantly, but we keep it clean)
        st.write("")
        st.markdown('<div class="glass">', unsafe_allow_html=True)
        st.subheader("Prediction")

        st.markdown(
            f"""
            <div class="badge">
              <span class="dot {dot_cls}"></span>
              <div>
                <div class="{color_cls}" style="font-weight:800; font-size:1.15rem;">
                  {icon} {level} Crowd – {occupancy}% seats full
                </div>
                <div class="muted">{marathi_line(level, occupancy)}</div>
              </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.markdown('<div class="barwrap">', unsafe_allow_html=True)
        st.markdown("**Occupancy**")
        st.progress(occupancy / 100.0)
        st.caption("Higher percentage means more crowd.")
        st.markdown("</div>", unsafe_allow_html=True)

        # Suggestion
        st.markdown("**Suggestion**")
        st.write(suggestion_en)
        st.write("**सूचना (Marathi):**")
        mr_sugg = {
            "High": "पीक वेळ टाळण्यासाठी लवकर/उशिरा प्रवास करण्याचा विचार करा.",
            "Medium": "बस मध्ये गर्दी असू शकते, पण सीट मिळण्याची शक्यता आहे.",
            "Low": "प्रवास आरामदायी होण्याची शक्यता जास्त आहे.",
        }[level]
        st.write(mr_sugg)

        # Optional badge: Best time suggestion
        st.markdown("---")
        st.markdown(f"**Best Time Suggestion:** {best_time}")

        st.markdown("</div>", unsafe_allow_html=True)
