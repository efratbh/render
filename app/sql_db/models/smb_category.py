from sqlalchemy import Column, Integer, ForeignKey
from app.sql_db.models import Base


class SmbCategory(Base):
    __tablename__ = 'smbs_categories'
    __table_args__ = {'schema': 'public'}

    category_id = Column(Integer, ForeignKey('public.categories.id'), primary_key=True)
    smb_id = Column(Integer, ForeignKey('public.smbs.id'), primary_key=True)

    def __repr__(self):
        return f'[SmbCategory: smb_id={self.smb_id} category_id={self.category_id}]'
