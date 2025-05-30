import csv

from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import sessionmaker
import numpy as np

from app.settings.sql_config import SQL_URL
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


def mysweetarithatilovesomuchhhhhhhhhhhh():
    with session_maker() as session:
        print(len(session.query(SmbCategory).all()))
        # session.execute(text('DROP TABLE transactions CASCADE;'))
        # session.commit()
        # smbs = session.query(Xtribution).all()
        #
        # if not smbs:
        #     print("לא נמצאו נתונים בטבלה Smb.")
        #     return
        #
        # # המרה לרשימת מילונים
        # data = [
        #     {column.name: getattr(smb, column.name) for column in Xtribution.__table__.columns}
        #     for smb in smbs
        # ]
        #
        # # המרה ל־DataFrame
        # df = pd.DataFrame(data)
        #
        # # שמירה ל־CSV בלי אינדקס מיותר
        # df.to_csv('xtribution.csv', index=False, encoding='utf-8')
        #
        # print(f"הנתונים נשמרו בהצלחה בקובץ: ")
        #

mysweetarithatilovesomuchhhhhhhhhhhh()




def import_csv_to_transactions(csv_path: str, max_rows: int = 40000):
    df = pd.read_csv(csv_path, encoding='utf-8', nrows=max_rows)

    # שמירה רק על עמודות שרלוונטיות למודל
    valid_columns = Transaction.__table__.columns.keys()
    df = df[[col for col in df.columns if col in valid_columns]]

    # המרת NaN ל־None
    df = df.replace({np.nan: None})

    successful_inserts = 0
    failed_rows = []

    with session_maker() as session:
        for index, row in df.iterrows():
            try:
                # המרת float ל־int אם הערך אמור להיות מספר שלם
                row_data = {
                    k: int(v) if isinstance(v, float) and v.is_integer() else v
                    for k, v in row.to_dict().items()
                }

                transaction = Transaction(**row_data)
                session.add(transaction)
                successful_inserts += 1

            except Exception as e:
                failed_rows.append((index + 1, str(e)))

        # ניסיון לבצע commit כולל
        try:
            session.commit()
            print(f"הוזנו בהצלחה {successful_inserts} רשומות מהקובץ {csv_path}")
        except SQLAlchemyError as e:
            session.rollback()
            print("❌ שגיאה ב־commit הסופי:")
            print(str(e))

    # סיכום
    if failed_rows:
        print(f"\n💥 {len(failed_rows)} שורות נכשלו:")
        for i, err in failed_rows[:10]:  # מדפיס רק את 10 הראשונות
            print(f"שורה {i}: {err}")

# קריאה לפונקציה
# import_csv_to_transactions('transaction.csv')

def check_problematic_rows_for_db(csv_path: str, max_rows: int = 20000):
    df = pd.read_csv(csv_path, encoding='utf-8', nrows=max_rows)

    # שמירה רק על עמודות שרלוונטיות למודל
    valid_columns = Transaction.__table__.columns.keys()
    df = df[[col for col in df.columns if col in valid_columns]]

    print(f"📄 בודק את {len(df)} השורות הראשונות בקובץ {csv_path}...")

    problematic_rows = []

    with session_maker() as session:
        for index, row in df.iterrows():
            try:
                transaction = Transaction(**row.to_dict())
                session.add(transaction)
                session.flush()  # ננסה לכתוב למסד אך בלי לבצע commit
                session.rollback()
            except SQLAlchemyError as e:
                problematic_rows.append((index + 1, row.to_dict(), str(e)))
                session.rollback()

    if problematic_rows:
        print(f"\n🔍 נמצאו {len(problematic_rows)} שורות בעייתיות מתוך {len(df)} שורות שנבדקו:\n")
        for idx, row_data, error in problematic_rows:
            print(f"שורה {idx}: ❌ שגיאה: {error}")
            print(f"  ➤ תוכן השורה: {row_data}\n")
    else:
        print(f"\n✅ לא נמצאו שורות בעייתיות. כל {len(df)} השורות נראות תקינות להכנסה למסד הנתונים.")

# קריאה לדוגמה
# check_problematic_rows_for_db('transaction.csv', max_rows=40000)
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