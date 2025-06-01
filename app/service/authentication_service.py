from app.sql_db.models.smb import Smb
from app.sql_db.repository.buisness_owner_repository import get_businness_owner_by_name_and_password


def check_if_password_correct(owner_full_name: str, password: str):
    try:
        biz_owner = get_businness_owner_by_name_and_password(owner_full_name=owner_full_name,
                                                             password=password)
        smb: Smb = biz_owner.smb

        return {"is_password_correct": True, "smb_id": smb[0].id} if biz_owner else False

    except Exception as e:
        print(str(e))
        return False
