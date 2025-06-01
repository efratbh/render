from app.sql_db.database import session_maker, engine
from app.sql_db.models.buisness_owner import BusinessOwner
from app.sql_db.models.category import Category
from app.sql_db.models.smb import Smb
from app.sql_db.models.smb_category import SmbCategory
from app.sql_db.models.transaction import Transaction
from app.sql_db.models.xtribution import Xtribution
import pandas as pd
from sqlalchemy import text

#here we will werite all the SQL queries


def get():
    with session_maker() as session:
        print(len(session.query(SmbCategory).all()))

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
def compare_new_customers(smb_id_target: int):
    with engine.connect() as connection:
        # שליפת הנתונים הרלוונטיים
        df = pd.read_sql(text("""
            SELECT create_date, smb_id, xtributer_id
            FROM transactions
        """), connection)

    # המרת תאריכים ל־UTC
    df['create_date'] = pd.to_datetime(df['create_date'], utc=True)

    # רכישה ראשונה של כל לקוח בכל עסק
    first_purchase = (
        df.groupby(['smb_id', 'xtributer_id'])['create_date']
        .min()
        .reset_index()
        .rename(columns={'create_date': 'first_date'})
    )

    # מיזוג חזרה עם הטבלה
    df = df.merge(first_purchase, on=['smb_id', 'xtributer_id'], how='left')

    # סיווג לקוחות
    df['customer_status'] = df.apply(
        lambda row: 'new' if row['create_date'] == row['first_date'] else 'returning',
        axis=1
    )

    # המרת תאריכים לחודשים
    df['month'] = df['create_date'].dt.to_period('M').dt.to_timestamp()

    # סינון רק לקוחות חדשים
    df_new = df[df['customer_status'] == 'new']

    # סיכום לפי חודש ועסק
    monthly_counts = (
        df_new.groupby(['month', 'smb_id'])['xtributer_id']
        .nunique()
        .reset_index()
        .rename(columns={'xtributer_id': 'num_customers'})
    )

    # נתוני עסק ספציפי
    smb_target = monthly_counts[monthly_counts['smb_id'] == smb_id_target][['month', 'num_customers']].rename(columns={'num_customers': 'smb_target'})

    # ממוצע שאר העסקים
    others_avg = (
        monthly_counts[monthly_counts['smb_id'] != smb_id_target]
        .groupby('month')['num_customers']
        .mean()
        .reset_index()
        .rename(columns={'num_customers': 'others_avg'})
    )

    # מיזוג סופי
    comparison_df = pd.merge(smb_target, others_avg, on='month')

    return comparison_df

# דוגמה לשימוש:
df = compare_new_customers(167)
print(df)
