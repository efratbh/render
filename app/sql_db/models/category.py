from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.sql_db.models import Base


class Category(Base):
    __tablename__ = 'categories'
    __table_args__ = {'schema': 'public'}

    id = Column(Integer, primary_key=True)
    type = Column(String)

    # חובה לציין את שם הסכימה בטבלת הקישור
    smbs = relationship('Smb', secondary='public.smbs_categories', back_populates='categories')

    def __repr__(self):
        return f'[Category: id={self.id} type={self.type}]'
