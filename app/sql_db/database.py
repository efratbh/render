from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.settings.sql_config import SQL_URL
from app.sql_db.models import Base

engine = create_engine(SQL_URL)
session_maker = sessionmaker(engine)

def init_db():
    Base.metadata.create_all(engine)
