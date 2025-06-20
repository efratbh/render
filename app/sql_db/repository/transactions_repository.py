from datetime import datetime
from sqlalchemy import func
from app.sql_db.database import session_maker
from app.sql_db.models.transaction import Transaction
from app.sql_db.models.smb_category import SmbCategory

def get_sum_transactions(smb_id: int, start_date: datetime, end_date: datetime) -> float:
    with session_maker() as session:
        total = session.query(func.sum(Transaction.total_amount)) \
            .filter(Transaction.smb_id == smb_id) \
            .filter(Transaction.create_date >= start_date) \
            .filter(Transaction.create_date < end_date) \
            .scalar()

    return float(total or 0)


def get_my_customers_count(smb_id: int, start_date: datetime, end_date: datetime):
    with session_maker() as session:
        return session.query(func.count(func.distinct(Transaction.xtributer_id))).filter(
            Transaction.smb_id == smb_id,
            Transaction.create_date >= start_date,
            Transaction.create_date <= end_date
        ).scalar() or 0

def get_similar_customers_avg(category_id: int, smb_id: int, start_date: datetime, end_date: datetime):
    with session_maker() as session:
        raw = session.query(func.count(func.distinct(Transaction.xtributer_id))).join(
            SmbCategory, Transaction.smb_id == SmbCategory.smb_id
        ).filter(
            SmbCategory.category_id == category_id,
            Transaction.smb_id != smb_id,
            Transaction.create_date >= start_date,
            Transaction.create_date <= end_date
        ).group_by(Transaction.smb_id).all()

        values = [r[0] for r in raw]

        return round(sum(values) / len(values), 1) if values else 0

def get_my_transaction_total(smb_id: int, start_date: datetime, end_date: datetime):
    with session_maker() as session:
        transactions = session.query(Transaction).filter(
            Transaction.smb_id == smb_id,
            Transaction.create_date >= start_date,
            Transaction.create_date <= end_date
        ).all()

        return round(sum(t.total_amount or 0 for t in transactions), 1)

def get_similar_transaction_avg(category_id: int, smb_id: int, start_date: datetime, end_date: datetime):
    with session_maker() as session:
        avg = session.query(func.avg(Transaction.total_amount)).join(
            SmbCategory, Transaction.smb_id == SmbCategory.smb_id
        ).filter(
            SmbCategory.category_id == category_id,
            Transaction.smb_id != smb_id,
            Transaction.create_date >= start_date,
            Transaction.create_date <= end_date
        ).scalar()

        return round(avg, 1) if avg else 0

def get_total_sales_amount_in_range(smb_id: int, start_date: datetime, end_date: datetime):
    with session_maker() as session:
        total = session.query(func.sum(Transaction.total_amount)) \
            .filter(Transaction.smb_id == smb_id) \
            .filter(Transaction.create_date >= start_date) \
            .filter(Transaction.create_date < end_date) \
            .scalar()

        return float(total or 0)
