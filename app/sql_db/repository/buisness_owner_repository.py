from sqlalchemy.orm import joinedload

from app.sql_db.database import session_maker
from app.sql_db.models.buisness_owner import BusinessOwner
from app.sql_db.models.category import Category
from app.sql_db.models.smb import Smb
from app.sql_db.models.smb_category import SmbCategory
from app.sql_db.models.transaction import Transaction
from app.sql_db.models.xtribution import Xtribution


def get_all_business_owners():
    with session_maker() as session:
        return session.query(BusinessOwner).all()

def get_business_owner_by_id(owner_id: int):
    with session_maker() as session:
        return session.query(BusinessOwner).filter_by(id=owner_id).first()

def get_businness_owner_by_name_and_password(owner_full_name: str, password: str):
    with session_maker() as session:
        return (
            session.query(BusinessOwner)
            .options(
                joinedload(BusinessOwner.smb).joinedload(Smb.categories)
                     )
            .filter_by(owner_full_name=owner_full_name, bn_number=password)
            .first()
        )

def create_business_owner(bn_number: str, owner_full_name: str, is_payment_established: bool,
                          payment_method_type: str, is_paying: bool):
    new_owner = BusinessOwner(
        bn_number=bn_number,
        owner_full_name=owner_full_name,
        is_payment_established=is_payment_established,
        payment_method_type=payment_method_type,
        is_paying=is_paying
    )

    with session_maker() as session:
        session.add(new_owner)
        session.commit()

    return new_owner

def update_business_owner(owner_id: int, **kwargs):
    with session_maker() as session:
        owner = session.query(BusinessOwner).filter_by(id=owner_id).first()

        if not owner:
            return None

        for key, value in kwargs.items():
            if hasattr(owner, key):
                setattr(owner, key, value)

        session.commit()

    return owner

def delete_business_owner(owner_id: int):
    with session_maker() as session:
        owner = session.query(BusinessOwner).filter_by(id=owner_id).first()

        if not owner:
            return False

        session.delete(owner)
        session.commit()

    return True
