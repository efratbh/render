from app.sql_db.database import session_maker
from app.sql_db.models.category import Category
from app.sql_db.models.smb import Smb
from app.sql_db.models.smb_category import SmbCategory
from app.sql_db.models.transaction import Transaction
from app.sql_db.models.xtribution import Xtribution
from app.sql_db.models.buisness_owner import BusinessOwner
from toolz import pipe, compose
import pandas as pd

def get_categories_by_smb_id(smb_id: int):
    with session_maker() as session:
        smb: Smb = session.query(Smb).filter(Smb.id == smb_id).first()
        if smb is None:
            print(f"SMB with id {smb_id} not found.")
            return []

        smb_categories_id: list = [category.id for category in smb.categories]

        return smb_categories_id
def get_smbs_ids_by_categories_id(categories_id: list[int]) -> list[int]:
    with session_maker() as session:
        smb_ids = (
            session.query(SmbCategory.smb_id)
            .filter(SmbCategory.category_id.in_(categories_id))
            .distinct()
            .all()
        )
        return [row[0] for row in smb_ids]


def get_create_data_xtributer_id_by_smbs_ids(smbs_ids: list[int]) -> list[dict]:
    with session_maker() as session:
        results = (
            session.query(
                Transaction.create_date,
                Transaction.smb_id,
                Transaction.xtributer_id
            )
            .filter(Transaction.smb_id.in_(smbs_ids))
            .all()
        )

        json_results = [
            {
                "create_date": row[0].isoformat() if row[0] else None,
                "smb_id": row[1],
                "xtributer_id": row[2]
            }
            for row in results
        ]

        return json_results



 # print(results)

def get_new_customers_comparison_json(json_data: list[dict], target_smb_id: int) -> list[dict]:
    import pandas as pd

    # המרה ל-DataFrame
    df = pd.DataFrame(json_data)
    df['create_date'] = pd.to_datetime(df['create_date'])
    df['month'] = df['create_date'].dt.to_period('M').dt.to_timestamp()

    # מציאת רכישה ראשונה
    first_purchase = (
        df.groupby(['smb_id', 'xtributer_id'])['create_date']
        .min()
        .reset_index()
        .rename(columns={'create_date': 'first_date'})
    )
    df = df.merge(first_purchase, on=['smb_id', 'xtributer_id'], how='left')
    df['customer_status'] = df.apply(
        lambda row: 'new' if row['create_date'] == row['first_date'] else 'returning',
        axis=1
    )

    # סיכום לקוחות חדשים לפי חודש ועסק
    summary = (
        df[df['customer_status'] == 'new']
        .groupby(['month', 'smb_id'])['xtributer_id']
        .nunique()
        .reset_index()
        .rename(columns={'xtributer_id': 'new_customers'})
    )

    # פיצול ליעד ואחרים
    target_df = summary[summary['smb_id'] == target_smb_id].copy()
    others_df = summary[summary['smb_id'] != target_smb_id].copy()

    # ממוצע שאר העסקים
    others_avg = (
        others_df
        .groupby('month')['new_customers']
        .mean()
        .reset_index()
        .rename(columns={'new_customers': 'others_avg'})
    )

    # מיזוג
    plot_df = target_df.merge(others_avg, on='month', how='left')
    plot_df = plot_df.rename(columns={'new_customers': 'smb_target'})

    # המרה ל־JSON מוכן לגרף
    plot_df['month'] = plot_df['month'].dt.strftime('%Y-%m')  # עיצוב חודש
    json_ready = plot_df.to_dict(orient='records')
    return json_ready
