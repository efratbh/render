from sqlalchemy import Column, Integer, true, String
from sqlalchemy.orm import relationship

from app.sql_db.models import Base


class Category(Base):
    __tablename__ = 'categories'
    id = Column(Integer, primary_key=True)
    type = Column(String)

    smbs = relationship('Smb', secondary="smbs_categories", back_populates='categories')

    def __repr__(self):# system function to print  list normal
        return f'[Category: id={self.id} type={self.type}]'
