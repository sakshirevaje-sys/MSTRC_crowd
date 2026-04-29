from datetime import date

def is_weekend(d):
    return 1 if d.weekday() >= 5 else 0

# Holidays with names
HOLIDAYS = {
    date(2026, 1, 26): "Republic Day",
    date(2026, 8, 15): "Independence Day",
    date(2026, 10, 2): "Gandhi Jayanti",
}

# Festivals with names
FESTIVALS = {
    date(2026, 9, 17): "Ganesh Chaturthi",
    date(2026, 11, 8): "Diwali",
    date(2026, 7, 1): "Ashadhi Wari",
}

def get_calendar_features(selected_date):
    return {
        "is_weekend": is_weekend(selected_date),
        "is_holiday": 1 if selected_date in HOLIDAYS else 0,
        "is_festival": 1 if selected_date in FESTIVALS else 0,
        "holiday_name": HOLIDAYS.get(selected_date, None),
        "festival_name": FESTIVALS.get(selected_date, None),
    }