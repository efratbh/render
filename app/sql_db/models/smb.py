from sqlalchemy import Column, Integer, Boolean, String, Numeric, Float, JSON, ForeignKey
from sqlalchemy.orm import relationship
from app.sql_db.models import Base


class Smb(Base):
    __tablename__ = 'smbs'
    __table_args__ = {'schema': 'public'}

    id = Column(Integer, primary_key=True)
    name = Column(String)
    discount_percent = Column(Numeric(5, 2))
    is_listed = Column(Boolean)
    xtribution_enabled = Column(Boolean)
    balance = Column(Numeric(15, 6))
    phone_number = Column(String)
    long = Column(Float)
    lat = Column(Float)
    address = Column(String)
    address_url = Column(String)
    social_urls = Column(String)
    type = Column(String)
    profile_pic = Column(String)
    biz_owner_id = Column(Integer, ForeignKey('public.biz_owners.id'))
    plan = Column(String)
    google_place_id = Column(String)
    external_data = Column(JSON)

    categories = relationship('Category', secondary='public.smbs_categories', back_populates='smbs')
    transactions = relationship('Transaction', back_populates='smb')
    xtributions = relationship('Xtribution', back_populates='smbs')
    biz_owners = relationship('BusinessOwner', back_populates='smb')

    def __repr__(self):
        return (f"<Smb id={self.id} name='{self.name}' type='{self.type}' "
                f"is_listed={self.is_listed} balance={self.balance} "
                f"lat={self.lat} long={self.long}>")
