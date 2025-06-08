from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
from zoneinfo import ZoneInfo
from sqlalchemy import func
from app.sql_db.models.transaction import Transaction

HEBREW_MONTHS = [
    "ינואר", "פברואר", "מרץ", "אפריל", "מאי", "יוני",
    "יולי", "אוגוסט", "ספטמבר", "אוקטובר", "נובמבר", "דצמבר"
]

def get_sum_for_range(session, smb_id, start_date, end_date):
    total = session.query(func.sum(Transaction.total_amount)) \
        .filter(Transaction.smb_id == smb_id) \
        .filter(Transaction.create_date >= start_date) \
        .filter(Transaction.create_date < end_date) \
        .scalar()
    return float(total or 0)

def get_weekly_sales_comparison_json(session, smb_id, end_date):
    data = []
    for i in range(7):
        current_day = end_date - timedelta(days=6 - i)
        past_week_day = current_day - timedelta(days=7)

        current_sum = get_sum_for_range(session, smb_id, current_day, current_day + timedelta(days=1))
        past_sum = get_sum_for_range(session, smb_id, past_week_day, past_week_day + timedelta(days=1))

        data.append({
            "date": current_day.strftime("%Y-%m-%d"),
            "current_week": current_sum,
            "previous_week": past_sum
        })
    return data

def get_weekly_sales_per_month_comparison_json(session, smb_id):
    data = []
    current_month = datetime(2023, 5, 1, tzinfo=ZoneInfo("Asia/Jerusalem"))
    previous_month = current_month - relativedelta(months=1)
    current_month_name = HEBREW_MONTHS[current_month.month - 1]
    previous_month_name = HEBREW_MONTHS[previous_month.month - 1]

    for week_index in range(4):
        current_start = current_month + timedelta(days=week_index * 7)
        current_end = current_start + timedelta(days=7)

        previous_start = previous_month + timedelta(days=week_index * 7)
        previous_end = previous_start + timedelta(days=7)

        current_sum = get_sum_for_range(session, smb_id, current_start, current_end)
        previous_sum = get_sum_for_range(session, smb_id, previous_start, previous_end)

        week_range_current = f"{current_start.day}-{(current_end - timedelta(days=1)).day}/{current_month.strftime('%m')}/{current_month.year}"
        week_range_previous = f"{previous_start.day}-{(previous_end - timedelta(days=1)).day}/{previous_month.strftime('%m')}/{previous_month.year}"

        data.append({
            "week": week_index + 1,
            "week_range_current_month": week_range_current,
            "week_range_previous_month": week_range_previous,
            "current_month_name": current_month_name,
            "previous_month_name": previous_month_name,
            "current_month_week_sales": current_sum,
            "previous_month_week_sales": previous_sum
        })

    return data

def get_yearly_sales_comparison_json(session, smb_id):
    data = []
    for month in range(1, 13):
        current_start = datetime(2023, month, 1, tzinfo=ZoneInfo("Asia/Jerusalem"))
        current_end = current_start + relativedelta(months=1)

        past_start = current_start - relativedelta(years=1)
        past_end = current_end - relativedelta(years=1)

        current_sum = get_sum_for_range(session, smb_id, current_start, current_end)
        past_sum = get_sum_for_range(session, smb_id, past_start, past_end)

        data.append({
            "month": HEBREW_MONTHS[month - 1],
            "sales_2023": current_sum,
            "sales_2022": past_sum
        })
    return data
