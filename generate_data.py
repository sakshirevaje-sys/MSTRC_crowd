# generate_data.py
import numpy as np
import pandas as pd
from datetime import datetime, timedelta

# ----------------------------
# 1. Configuration
# ----------------------------
np.random.seed(42)

routes = [
    {"route": "Solapur-Pune", "distance_km": 260, "stops": 10},
    {"route": "Solapur-Kolhapur", "distance_km": 230, "stops": 9},
    {"route": "Solapur-Akkalkot", "distance_km": 40, "stops": 5},
    {"route": "Solapur-Pandharpur", "distance_km": 70, "stops": 6},
    {"route": "Solapur-Latur", "distance_km": 110, "stops": 7},
    {"route": "Solapur-Sangli", "distance_km": 210, "stops": 8},
]

start_date = datetime(2025, 4, 1)
end_date = datetime(2026, 3, 31)

# Time slots (24‑hour)
time_slots = [6, 7, 8, 9, 12, 13, 14, 17, 18, 19]

# Maharashtra 2026 important holidays (approx; mini project level)
maharashtra_holidays_2026 = {
    datetime(2026, 1, 26).date(),  # Republic Day [web:10]
    datetime(2026, 3, 19).date(),  # Gudi Padwa [web:10]
    datetime(2026, 3, 21).date(),  # Ramzan-Id [web:10]
}

# Festival / special dates (custom for project)
festival_dates = {
    # Ganpati (example range)
    datetime(2025, 9, 7).date(),
    datetime(2025, 9, 8).date(),
    datetime(2025, 9, 9).date(),
    # Diwali (approx)
    datetime(2025, 10, 29).date(),
    datetime(2025, 10, 30).date(),
    # Ashadhi Wari towards Pandharpur (approx)
    datetime(2025, 7, 10).date(),
    datetime(2025, 7, 11).date(),
}

def get_base_crowd_level(hour, day_of_week, is_holiday, is_festival, route_name):
    """
    Returns 'Low' / 'Medium' / 'High' based on hand‑crafted rules.
    """
    # Start with Medium
    score = 0

    # Office hours peak – weekdays
    if day_of_week < 5:  # 0=Monday
        if 7 <= hour <= 9 or 17 <= hour <= 20:
            score += 2
        elif 6 <= hour <= 10 or 16 <= hour <= 21:
            score += 1

    # Noon off‑peak
    if 12 <= hour <= 15:
        score -= 1

    # Weekend effect
    if day_of_week >= 5:
        score += 0  # neutral; will adjust with route / festival

    # Holiday effect
    if is_holiday:
        score += 1

    # Festival effect
    if is_festival:
        score += 2

    # Pilgrimage routes (Pandharpur, Akkalkot)
    if "Pandharpur" in route_name or "Akkalkot" in route_name:
        score += 1
        if is_festival or is_holiday or day_of_week in (5, 6):  # Sat/Sun
            score += 1

    # Add some random noise
    score += np.random.choice([-1, 0, 1], p=[0.2, 0.6, 0.2])

    if score <= -1:
        return "Low"
    elif score <= 1:
        return "Medium"
    else:
        return "High"

def main():
    rows = []
    current = start_date
    while current <= end_date:
        date = current.date()
        day_of_week = current.weekday()
        is_weekend = 1 if day_of_week >= 5 else 0
        is_holiday = 1 if date in maharashtra_holidays_2026 else 0
        is_festival = 1 if date in festival_dates else 0

        weather_options = ["Clear", "Cloudy", "Rain", "Heavy Rain"]
        for rt in routes:
            for hour in time_slots:
                crowd_level = get_base_crowd_level(
                    hour,
                    day_of_week,
                    is_holiday,
                    is_festival,
                    rt["route"],
                )

                # Map qualitative crowd to approximate percentage (for reference)
                if crowd_level == "Low":
                    crowd_pct = np.random.randint(10, 40)
                elif crowd_level == "Medium":
                    crowd_pct = np.random.randint(40, 75)
                else:
                    crowd_pct = np.random.randint(75, 105)  # allow slight >100 for standing

                row = {
                    "date": date.isoformat(),
                    "route": rt["route"],
                    "day_of_week": day_of_week,
                    "hour": hour,
                    "is_weekend": is_weekend,
                    "is_holiday": is_holiday,
                    "is_festival": is_festival,
                    "distance_km": rt["distance_km"],
                    "num_stops": rt["stops"],
                    "weather": np.random.choice(weather_options, p=[0.5, 0.25, 0.2, 0.05]),
                    "crowd_level": crowd_level,
                    "crowd_percentage": crowd_pct,
                }
                rows.append(row)

        current += timedelta(days=1)

    df = pd.DataFrame(rows)

    # Create folder if not exists
    import os
    os.makedirs("data", exist_ok=True)

    df.to_csv("data/msrtc_crowd_data.csv", index=False)
    print("Saved data/msrtc_crowd_data.csv with", len(df), "rows")

if __name__ == "__main__":
    main()