from toolz import pipe
import pandas as pd
from app.sql_db.repository.smb_repository_repository import get_categories_by_smb_id, get_smbs_ids_by_categories_id, \
    get_create_data_xtributer_id_by_smbs_ids


def get_smbs_details_with_same_categories_by_smb_id(smb_id: int):
    return pipe(
            smb_id,
            get_categories_by_smb_id,
            get_smbs_ids_by_categories_id,
            get_create_data_xtributer_id_by_smbs_ids
    )

def get_new_customers_comparison_json(json_data: list[dict], target_smb_id: int, period_type: str) -> list[dict]:
    df = prepare_dataframe(json_data=json_data, period_type=period_type)
    df = add_customer_status(df=df)
    summary = summarize_customers(df=df)
    target_df, others_df = split_target_vs_others(summary=summary, target_smb_id=target_smb_id)
    return build_plot_data(target_df=target_df, others_df=others_df, period_type=period_type)

def prepare_dataframe(json_data: list[dict], period_type: str) -> pd.DataFrame:
    df = pd.DataFrame(json_data)
    df['create_date'] = pd.to_datetime(df['create_date'])
    df['period'] = (
        df['create_date'].dt.to_period('W').dt.start_time
        if period_type == 'week'
        else df['create_date'].dt.to_period('M').dt.to_timestamp()
    )
    return df

def add_customer_status(df: pd.DataFrame) -> pd.DataFrame:
    first_purchase = (
        df.groupby(['smb_id', 'xtributer_id'])['create_date']
        .min()
        .reset_index()
        .rename(columns={'create_date': 'first_date'})
    )
    df = df.merge(first_purchase, on=['smb_id', 'xtributer_id'], how='left')
    df['customer_status'] = df.apply(
        lambda row: 'new' if row['create_date'] == row['first_date'] else 'returning', axis=1
    )
    return df

def summarize_customers(df: pd.DataFrame) -> pd.DataFrame:
    new_summary = (
        df[df['customer_status'] == 'new']
        .groupby(['period', 'smb_id'])['xtributer_id']
        .nunique()
        .reset_index()
        .rename(columns={'xtributer_id': 'new_customers'})
    )
    returning_summary = (
        df[df['customer_status'] == 'returning']
        .groupby(['period', 'smb_id'])['xtributer_id']
        .nunique()
        .reset_index()
        .rename(columns={'xtributer_id': 'returning_customers'})
    )
    return pd.merge(new_summary, returning_summary, on=['period', 'smb_id'], how='outer').fillna(0)

def split_target_vs_others(summary: pd.DataFrame, target_smb_id: int):
    target_df = summary[summary['smb_id'] == target_smb_id].copy()
    others_df = summary[summary['smb_id'] != target_smb_id].copy()
    return target_df, others_df

def build_plot_data(target_df: pd.DataFrame, others_df: pd.DataFrame, period_type: str) -> list[dict]:
    others_avg = (
        others_df
        .groupby('period')[['new_customers', 'returning_customers']]
        .mean()
        .reset_index()
        .rename(columns={
            'new_customers': 'others_avg_new',
            'returning_customers': 'others_avg_returning'
        })
    )
    if target_df.empty:
        raise Exception('No transactions were found for this store.')

    target_df = target_df.rename(columns={
        'new_customers': 'smb_target_new',
        'returning_customers': 'smb_target_returning'
    })
    plot_df = target_df.merge(others_avg, on='period', how='left')
    plot_df['period'] = plot_df['period'].dt.strftime('%Y-%m-%dT00:00:00.000Z')

    result = []
    for _, row in plot_df.iterrows():
        result.append({
            "month" if period_type == 'month' else "week": row['period'],
            "smb_target": {
                "avg_new_customers": round(row['smb_target_new'], 1),
                "avg_returning_customers": round(row['smb_target_returning'], 1)
            },
            "others": {
                "avg_new_customers": round(row['others_avg_new'], 1) if pd.notnull(row['others_avg_new']) else None,
                "avg_returning_customers": round(row['others_avg_returning'], 1) if pd.notnull(row['others_avg_returning']) else None
            }
        })
    return result


def get_monthly_new_customers_analysis(smb_id: int) -> list[dict]:
    transactions_data = get_smbs_details_with_same_categories_by_smb_id(smb_id=smb_id)

    chart_json: list[dict] = get_new_customers_comparison_json(json_data=transactions_data,
                                                               target_smb_id=smb_id,
                                                               period_type='month')

    return chart_json

def get_weekly_new_customers_analysis(smb_id: int) -> list[dict]:
    transactions_data = get_smbs_details_with_same_categories_by_smb_id(smb_id=smb_id)

    chart_json: list[dict] = get_new_customers_comparison_json(json_data=transactions_data,
                                                               target_smb_id=smb_id,
                                                               period_type='week')

    return chart_json
