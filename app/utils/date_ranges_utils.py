from datetime import datetime, timedelta
from zoneinfo import ZoneInfo
import pandas as pd

def get_all_month_ranges():
    now = datetime(2024, 6, 1, tzinfo=ZoneInfo("Asia/Jerusalem"))
    months = []
    for m in range(1, now.month + 1):
        start = datetime(now.year, m, 1, tzinfo=ZoneInfo("Asia/Jerusalem"))
        if m == 12:
            end = datetime(now.year + 1, 1, 1, tzinfo=ZoneInfo("Asia/Jerusalem")) - timedelta(days=1)
        else:
            end = datetime(now.year, m + 1, 1, tzinfo=ZoneInfo("Asia/Jerusalem")) - timedelta(days=1)
        months.append((start, end))
    return months

def get_all_valid_weeks():
    today = datetime(2024, 6, 1, tzinfo=ZoneInfo("Asia/Jerusalem"))
    start_of_month = today.replace(day=1)
    next_month = (start_of_month + timedelta(days=32)).replace(day=1)
    weeks = []
    current_date = start_of_month
    while current_date < next_month:
        if current_date.weekday() == 6:  # Sunday
            week_start = current_date
            week_end = week_start + timedelta(days=6)
            days_in_month = [d for d in pd.date_range(week_start, week_end) if d.month == today.month]
            if len(days_in_month) >= 3:
                weeks.append((week_start, week_end))
        current_date += timedelta(days=1)
    return weeks
