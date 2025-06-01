from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import relationship
from app.sql_db.models import Base


class BusinessOwner(Base):
    __tablename__ = 'biz_owners'
    __table_args__ = {'schema': 'public'}

    id = Column(Integer, primary_key=True)
    bn_number = Column(String)
    owner_full_name = Column(String)
    is_payment_established = Column(Boolean)
    payment_method_type = Column(String)
    is_paying = Column(Boolean)

    # נגדיר את הקשר מבלי לייבא את Smb ישירות כדי להימנע ממעגליות
    smb = relationship('Smb', back_populates='biz_owners')

    def __repr__(self):
        return (
            f"<BusinessOwner(id={self.id}, "
            f"bn_number='{self.bn_number}', "
            f"owner_full_name='{self.owner_full_name}', "
            f"is_payment_established={self.is_payment_established}, "
            f"payment_method_type='{self.payment_method_type}', "
            f"is_paying={self.is_paying})>"
        )
