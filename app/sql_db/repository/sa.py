from app.sql_db.database import session_maker
from app.sql_db.models.buisness_owner import BusinessOwner
from app.sql_db.models.category import Category
from app.sql_db.models.smb import Smb
from app.sql_db.models.smb_category import SmbCategory
from app.sql_db.models.transaction import Transaction
from app.sql_db.models.xtribution import Xtribution
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo
from sqlalchemy import func
import json
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


def get_category_id(session, smb_id):
    result = session.query(SmbCategory.category_id).filter(SmbCategory.smb_id == smb_id).first()
    return result[0] if result else None



def weekly_sales_comparison(smb_id):
    return compare_sales(smb_id, get_all_valid_weeks())

def monthly_sales_comparison(smb_id):
    return compare_sales(smb_id, get_all_month_ranges())

def weekly_customers_comparison(smb_id):
    return compare_customers(smb_id, get_all_valid_weeks())

def monthly_customers_comparison(smb_id):
    return compare_customers(smb_id, get_all_month_ranges())

def weekly_recommendations_comparison(smb_id):
    return compare_recommendations(smb_id, get_all_valid_weeks())

def monthly_recommendations_comparison(smb_id):
    return compare_recommendations(smb_id, get_all_month_ranges())



def compare_customers(smb_id, ranges):
    results = []
    with session_maker() as session:
        category_id = get_category_id(session, smb_id)
        if not category_id:
            return [{"error": f"לא נמצאה קטגוריה לעסק {smb_id}"}]

        for start_date, end_date in ranges:
            my_customers_count = session.query(func.count(func.distinct(Transaction.xtributer_id))).filter(
                Transaction.smb_id == smb_id,
                Transaction.create_date >= start_date,
                Transaction.create_date <= end_date
            ).scalar() or 0

            similar_customers_avg = session.query(func.count(func.distinct(Transaction.xtributer_id))).join(
                SmbCategory, Transaction.smb_id == SmbCategory.smb_id
            ).filter(
                SmbCategory.category_id == category_id,
                Transaction.smb_id != smb_id,
                Transaction.create_date >= start_date,
                Transaction.create_date <= end_date
            ).group_by(Transaction.smb_id).all()

            values = [row[0] for row in similar_customers_avg]
            avg = round(sum(values) / len(values), 1) if values else 0

            results.append({
                "start_date": start_date.isoformat(),
                "end_date": end_date.isoformat(),
                "my_customers_count": round(my_customers_count, 1),
                "similar_avg_customers_count": avg
            })
    return results



def compare_sales(smb_id, ranges):
    results = []
    with session_maker() as session:
        category_id = get_category_id(session, smb_id)
        if not category_id:
            return [{"error": f"לא נמצאה קטגוריה לעסק {smb_id}"}]

        for start_date, end_date in ranges:
            transactions = session.query(Transaction).filter(
                Transaction.smb_id == smb_id,
                Transaction.create_date >= start_date,
                Transaction.create_date <= end_date
            ).all()

            avg_amount = session.query(func.avg(Transaction.total_amount)).join(
                SmbCategory, Transaction.smb_id == SmbCategory.smb_id
            ).filter(
                SmbCategory.category_id == category_id,
                Transaction.smb_id != smb_id,
                Transaction.create_date >= start_date,
                Transaction.create_date <= end_date
            ).scalar()

            my_total = round(sum([t.total_amount or 0 for t in transactions]), 1)
            similar_avg = round(avg_amount, 1) if avg_amount else 0

            results.append({
                "start_date": start_date.isoformat(),
                "end_date": end_date.isoformat(),
                "my_total_transaction_amount": my_total,
                "similar_avg_transaction_amount": similar_avg
            })
    return results



def compare_recommendations(smb_id, ranges):
    results = []
    with session_maker() as session:
        category_id = get_category_id(session, smb_id)
        if not category_id:
            return [{"error": f"לא נמצאה קטגוריה לעסק {smb_id}"}]

        for start_date, end_date in ranges:
            my_recs_count = session.query(func.count(Xtribution.id)).filter(
                Xtribution.smb_id == smb_id,
                Xtribution.create_date >= start_date,
                Xtribution.create_date <= end_date
            ).scalar()

            similar_recs_avg = session.query(func.count(Xtribution.id)).join(
                SmbCategory, Xtribution.smb_id == SmbCategory.smb_id
            ).filter(
                SmbCategory.category_id == category_id,
                Xtribution.smb_id != smb_id,
                Xtribution.create_date >= start_date,
                Xtribution.create_date <= end_date
            ).group_by(Xtribution.smb_id).all()

            avg_similar = round(sum([x[0] for x in similar_recs_avg]) / len(similar_recs_avg), 1) if similar_recs_avg else 0

            results.append({
                "start_date": start_date.isoformat(),
                "end_date": end_date.isoformat(),
                "my_recommendations_count": round(my_recs_count, 1),
                "similar_avg_recommendations_count": avg_similar
            })
    return results
