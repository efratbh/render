from datetime import datetime

from sqlalchemy import func
from app.sql_db.database import session_maker
from app.sql_db.models.xtribution import Xtribution
from app.sql_db.models.buisness_owner import BusinessOwner
from app.sql_db.models.smb_category import SmbCategory
from app.sql_db.models.category import Category
from app.sql_db.models.smb import Smb
from app.sql_db.models.transaction import Transaction


def get_all_xtribution_ids_tuple():
    with session_maker() as session:
        return session.query(Xtribution.id).all()

def get_all_xtribution_ids() -> list[int]:
    all_xtribution_ids_tuple: list = get_all_xtribution_ids_tuple()
    xtribution_ids = []
    for id in all_xtribution_ids_tuple:
        xtribution_ids.append(id[0])
    return xtribution_ids

def get_my_recommendation_count(smb_id: int, start_date: datetime, end_date: datetime):
    with session_maker() as session:
        return session.query(func.count(Xtribution.id)).filter(
            Xtribution.smb_id == smb_id,
            Xtribution.create_date >= start_date,
            Xtribution.create_date <= end_date
        ).scalar() or 0

def get_similar_recommendations_avg(category_id: int, smb_id: int, start_date: datetime, end_date: datetime):
    with session_maker() as session:
        raw = session.query(func.count(Xtribution.id)).join(
            SmbCategory, Xtribution.smb_id == SmbCategory.smb_id
        ).filter(
            SmbCategory.category_id == category_id,
            Xtribution.smb_id != smb_id,
            Xtribution.create_date >= start_date,
            Xtribution.create_date <= end_date
        ).group_by(Xtribution.smb_id).all()

        values = [r[0] for r in raw]

        return round(sum(values) / len(values), 1) if values else 0
