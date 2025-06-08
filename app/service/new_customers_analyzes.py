from toolz import pipe

from app.sql_db.repository.smb_repository_repository import get_categories_by_smb_id, get_smbs_ids_by_categories_id, \
    get_create_data_xtributer_id_by_smbs_ids


def get_smbs_details_with_same_categories_by_smb_id(smb_id: int):
    return pipe(
            smb_id,
            get_categories_by_smb_id,
            get_smbs_ids_by_categories_id,
            get_create_data_xtributer_id_by_smbs_ids
    )

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

    # המרה ל־JSON מוכן לגרף — עם תאריך כ-ISO8601
    plot_df['month'] = plot_df['month'].dt.strftime('%Y-%m-01T00:00:00.000Z')

    json_ready = plot_df.to_dict(orient='records')
    return json_ready


def get_monthly_new_customers_analysis(smb_id: int) -> list[dict]:
    transactions_data = get_smbs_details_with_same_categories_by_smb_id(smb_id)

    chart_json = get_new_customers_comparison_json(transactions_data, smb_id)

    return chart_json

