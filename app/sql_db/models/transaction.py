from sqlalchemy import Column, Integer, String, Numeric, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.sql_db.models import Base


class Transaction(Base):
    __tablename__ = 'transactions'
    __table_args__ = {'schema': 'public'}

    id = Column(Integer, primary_key=True)
    status = Column(String)
    token_amount = Column(Numeric(15, 6))
    total_amount = Column(Numeric(10, 4))
    handled_by_user_id = Column(Integer)
    xtributer_id = Column(Integer)
    smb_id = Column(Integer, ForeignKey('public.smbs.id'))
    xtribution_id = Column(Integer, ForeignKey('public.xtributions.id'))
    create_date = Column(DateTime)
    update_date = Column(DateTime)
    foundation_id = Column(Integer)
    invoice_id = Column(Integer)
    is_promotional = Column(Boolean)

    smb = relationship('Smb', back_populates='transactions')
    xtribution = relationship('Xtribution', back_populates='transaction')

    def __repr__(self):
        return (
            f"<Transaction(id={self.id}, status='{self.status}', token_amount={self.token_amount}, "
            f"total_amount={self.total_amount}, smb_id={self.smb_id}, is_promotional={self.is_promotional})>"
        )
