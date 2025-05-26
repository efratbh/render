from sqlalchemy import Column, Integer, true, String
from sqlalchemy.orm import relationship
from sqlalchemy import ForeignKey
from app.sql_db.models import Base


class Smb_category(Base):
    __tablename__ = 'smbs_categories'
    smb_id = Column(Integer, ForeignKey('smbs.id'), primary_key=True)
    category_id = Column(Integer, ForeignKey('categories.id'), primary_key=True)

    # category_type = relationship('smbs_categories.category_id', )
    def __repr__(self):# system function to print  list normal
        return f'[Smb_category: smb_id={self.smb_id} category_id={self.category_id}]'

