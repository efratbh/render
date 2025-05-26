from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.settings.sql_config import SQL_URL
from app.sql_db.models import Base

engine = create_engine(SQL_URL) #connection with SQL
session_maker = sessionmaker(engine) #SESSION IS A -kind of ecsicute and then it creates a ssesion

def init_db():
    Base.metadata.create_all(engine)# connect to the base(objects-tables and bring them)
