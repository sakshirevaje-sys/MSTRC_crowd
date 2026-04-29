import pandas as pd
from datetime import datetime

TIMETABLE_PATH = "data/bus_timetable.csv"

def load_timetable():
    return pd.read_csv(TIMETABLE_PATH, dtype={"departure_time": str})


def clean_time_format(t):
    t = str(t).strip()

    if len(t.split(":")) == 3:
        t = ":".join(t.split(":")[:2])

    return t


def get_next_bus(route, selected_time_str, timetable_df):
    route_data = timetable_df[timetable_df["route"] == route]

    selected_time = datetime.strptime(selected_time_str, "%H:%M")

    future_times = []

    for t in route_data["departure_time"]:
        try:
            t_clean = clean_time_format(t)
            bus_time = datetime.strptime(t_clean, "%H:%M")

            if bus_time > selected_time:
                future_times.append(bus_time)

        except:
            continue

    if future_times:
        return min(future_times).strftime("%H:%M")

    return None