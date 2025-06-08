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

def get_date_range(days_back: int):
    end_date = datetime(2023, 5, 1, tzinfo=ZoneInfo("Asia/Jerusalem"))
    start_date = end_date - timedelta(days=days_back)
    return start_date, end_date

def get_category_id(session, smb_id):
    result = session.query(SmbCategory.category_id).filter(SmbCategory.smb_id == smb_id).first()
    return result[0] if result else None

def compare_sales(smb_id, days_back):
    start_date, end_date = get_date_range(days_back)
    with session_maker() as session:
        transactions = session.query(Transaction).filter(
            Transaction.smb_id == smb_id,
            Transaction.create_date >= start_date,
            Transaction.create_date <= end_date
        ).all()

        category_id = get_category_id(session, smb_id)
        if not category_id:
            return {"error": f"לא נמצאה קטגוריה לעסק {smb_id}"}

        avg_amount = session.query(func.avg(Transaction.total_amount)).join(
            SmbCategory, Transaction.smb_id == SmbCategory.smb_id
        ).filter(
            SmbCategory.category_id == category_id,
            Transaction.smb_id != smb_id,
            Transaction.create_date >= start_date,
            Transaction.create_date <= end_date
        ).scalar()

        my_total = round(sum([t.total_amount for t in transactions]))

        return {
            "smb_id": smb_id,
            "start_date": start_date.isoformat(),
            "end_date": end_date.isoformat(),
            "my_total_transaction_amount": my_total,
            "similar_avg_transaction_amount": round(avg_amount) if avg_amount else 0
        }

def compare_customers(smb_id, days_back):
    start_date, end_date = get_date_range(days_back)
    with session_maker() as session:
        category_id = get_category_id(session, smb_id)
        if not category_id:
            return {"error": f"לא נמצאה קטגוריה לעסק {smb_id}"}

        my_customers_count = session.query(func.count(func.distinct(Transaction.xtributer_id))).filter(
            Transaction.smb_id == smb_id,
            Transaction.create_date >= start_date,
            Transaction.create_date <= end_date
        ).scalar()

        similar_customers_avg = session.query(func.count(func.distinct(Transaction.xtributer_id))).join(
            SmbCategory, Transaction.smb_id == SmbCategory.smb_id
        ).filter(
            SmbCategory.category_id == category_id,
            Transaction.smb_id != smb_id,
            Transaction.create_date >= start_date,
            Transaction.create_date <= end_date
        ).group_by(Transaction.smb_id).all()

        if similar_customers_avg:
            similar_customers_avg_value = sum([x[0] for x in similar_customers_avg]) / len(similar_customers_avg)
        else:
            similar_customers_avg_value = 0

        return {
            "smb_id": smb_id,
            "start_date": start_date.isoformat(),
            "end_date": end_date.isoformat(),
            "my_customers_count": round(my_customers_count),
            "similar_avg_customers_count": round(similar_customers_avg_value)
        }

def compare_recommendations(smb_id, days_back):
    start_date, end_date = get_date_range(days_back)
    with session_maker() as session:
        category_id = get_category_id(session, smb_id)
        if not category_id:
            return {"error": f"לא נמצאה קטגוריה לעסק {smb_id}"}

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

        if similar_recs_avg:
            avg_similar = sum([x[0] for x in similar_recs_avg]) / len(similar_recs_avg)
        else:
            avg_similar = 0

        return {
            "smb_id": smb_id,
            "start_date": start_date.isoformat(),
            "end_date": end_date.isoformat(),
            "my_recommendations_count": round(my_recs_count),
            "similar_avg_recommendations_count": round(avg_similar)
        }

def weekly_sales_comparison(smb_id): return compare_sales(smb_id, 7)
def monthly_sales_comparison(smb_id): return compare_sales(smb_id, 30)

def weekly_customers_comparison(smb_id): return compare_customers(smb_id, 7)
def monthly_customers_comparison(smb_id): return compare_customers(smb_id, 30)

def weekly_recommendations_comparison(smb_id): return compare_recommendations(smb_id, 7)
def monthly_recommendations_comparison(smb_id): return compare_recommendations(smb_id, 30)

if __name__ == "__main__":
    smb_id = int(input("🔢 הכנס מזהה עסק: "))
    result = weekly_sales_comparison(smb_id)
    print(json.dumps(result, ensure_ascii=False, indent=2, default=str))
