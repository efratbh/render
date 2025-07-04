import json

from app.sql_db.models.category import Category
from app.sql_db.models.smb import Smb
from app.sql_db.repository.buisness_owner_repository import get_businness_owner_by_name_and_password


def check_if_password_correct(owner_full_name: str, password: str):
    try:
        biz_owner = get_businness_owner_by_name_and_password(owner_full_name=owner_full_name,
                                                             password=password)
        smb: Smb = biz_owner.smb[0]
        smb_id: int = smb.id
        smb_address_hebrew_name = json.loads(smb.address).get('he', '')
        smb_phone_number: str = smb.phone_number
        smb_categories: list[str] = [ca.type for ca in smb.categories]
        smb_hebrew_name: str = json.loads(smb.name).get('he', '')

        all_details: dict = {"is_password_correct": True, "smb_id": smb_id, "smb_name": smb_hebrew_name,
                             'owner_full_name': owner_full_name, 'categories': smb_categories,
                             'smb_address': smb_address_hebrew_name, 'smb_phone_number': smb_phone_number
                             }

        return all_details if biz_owner else False

    except Exception as e:
        print(str(e))
        return False
print(check_if_password_correct(owner_full_name='יעקופ עמיאני', password='317252120'))