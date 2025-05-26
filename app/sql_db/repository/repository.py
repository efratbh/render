from app.sql_db.database import session_maker, engine
from app.sql_db.models.buisness_owner import BusinessOwner
from app.sql_db.models.category import Category
from app.sql_db.models.smb import Smb
from app.sql_db.models.smb_category import Smb_category
from app.sql_db.models.transaction import Transaction
from app.sql_db.models.xtribution import Xtribution
import pandas as pd

#here we will werite all the SQL queries

def mysweetarithatilovesomuchhhhhhhhhhhh():
    with session_maker() as session:
        efrat = session.query(BusinessOwner).all()
        print(efrat)

mysweetarithatilovesomuchhhhhhhhhhhh()
def da():
    df = pd.read_sql("SELECT create_date, SMB_ID, XTRIBUTER_ID FROM transactions", engine.connect())

    # המרה ל-UTC כדי להימנע מבעיות timezone
    df['create_date'] = pd.to_datetime(df['create_date'], utc=True)

    first_purchase = (
        df.groupby(['smb_id', 'xtributer_id'])['create_date']
        .min()
        .reset_index()
        .rename(columns={'create_date': 'first_date'})
    )
    # גם כאן, לוודא ש-first_date ב-UTC
    first_purchase['first_date'] = pd.to_datetime(first_purchase['first_date'], utc=True)

    df = df.merge(first_purchase, on=['smb_id', 'xtributer_id'], how='left')

    df['customer_status'] = df.apply(
        lambda row: 'new' if row['create_date'] == row['first_date'] else 'returning',
        axis=1
    )

    df['month'] = df['create_date'].dt.to_period('M')

    summary = (
        df.groupby(['month', 'smb_id', 'customer_status'])['xtributer_id']
        .nunique()
        .reset_index()
        .rename(columns={'xtributer_id': 'num_customers'})
    )

    summary['month'] = summary['month'].dt.to_timestamp()

    print(summary)



# da()