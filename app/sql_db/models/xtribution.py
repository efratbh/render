from sqlalchemy import Column, Integer, String, Numeric, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.sql_db.models import Base


class Xtribution(Base):
    __tablename__ = 'xtributions'
    __table_args__ = {'schema': 'public'}

    id = Column(Integer, primary_key=True)
    status = Column(String)
    current_amount = Column(Numeric(15, 6))
    uuid = Column(String)
    photo_url = Column(String)
    xtributer_id = Column(Integer)
    smb_id = Column(Integer, ForeignKey('public.smbs.id'))  # ✅ schema נוסף
    create_date = Column(DateTime)
    end_date = Column(DateTime)
    dynamic_link = Column(String)
    type = Column(String)
    blurhash = Column(String)
    discount_percent = Column(Integer)

    smbs = relationship('Smb', back_populates='xtributions')
    transaction = relationship('Transaction', back_populates='xtribution')

    def __repr__(self):
        return (
            f"<Xtribution(id={self.id}, status='{self.status}', current_amount={self.current_amount}, "
            f"uuid='{self.uuid}', type='{self.type}', discount_percent={self.discount_percent})>"
        )
