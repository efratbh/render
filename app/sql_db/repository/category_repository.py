from app.sql_db.database import session_maker
from app.sql_db.models.smb_category import SmbCategory

def get_category_id(smb_id: int):
    with session_maker() as session:
        result = session.query(SmbCategory.category_id).filter(SmbCategory.smb_id == smb_id).first()
        return result[0] if result else None
