import json
from typing import Literal
import pandas as pd
import holidays
from datetime import datetime
from xgboost import XGBRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score

from app.sql_db.repository.transactions_repository import get_all_transactions_by_smb_id
from app.sql_db.models.xtribution import Xtribution
from app.sql_db.models.buisness_owner import BusinessOwner
from app.sql_db.models.smb_category import SmbCategory
from app.sql_db.models.category import Category
from app.sql_db.models.smb import Smb
from app.sql_db.models.transaction import Transaction


def sales_forecast_weekly(smb_id: int):
    return predict_transactions_for_smb(smb_id=smb_id, time_range='weekly')

def sales_forecast_monthly(smb_id: int):
    return predict_transactions_for_smb(smb_id=smb_id, time_range='monthly')

def predict_transactions_for_smb(smb_id: int, time_range: Literal["weekly", "monthly"] = "weekly") -> pd.DataFrame:
    # 1. שליפת נתונים
    all_transactions_by_smb_id = get_all_transactions_by_smb_id(smb_id=smb_id)
    all_transactions_filter = [
        [t.smb_id, t.total_amount, t.create_date]
        for t in all_transactions_by_smb_id
    ]
    df = pd.DataFrame(all_transactions_filter, columns=['smb_id', 'total_amount', 'create_date'])
    df['create_date'] = pd.to_datetime(df['create_date'], utc=True)
    df['date'] = df['create_date'].dt.date

    # 2. מאפייני תאריך יומי
    daily = df.groupby(['date']).size().reset_index(name='transaction_count')
    daily['day_of_week'] = pd.to_datetime(daily['date']).dt.dayofweek.apply(lambda x: 1 if x == 6 else x + 2)
    daily['day_of_month'] = pd.to_datetime(daily['date']).dt.day
    daily['month'] = pd.to_datetime(daily['date']).dt.month
    daily['is_weekend'] = daily['day_of_week'].isin([6, 7]).astype(int)
    daily['is_start_of_month'] = (daily['day_of_month'] <= 3).astype(int)
    daily['is_end_of_month'] = (daily['day_of_month'] >= 28).astype(int)

    # 3. חגים
    israel_holidays = pd.to_datetime(list(holidays.country_holidays('IL', years=[2023, 2024, 2025]).keys()))
    daily['is_christmas'] = daily['date'].apply(lambda d: 1 if d.month == 12 and d.day == 25 else 0)
    daily['is_valentines'] = daily['date'].apply(lambda d: 1 if d.month == 2 and d.day == 14 else 0)
    daily['is_womens_day'] = daily['date'].apply(lambda d: 1 if d.month == 3 and d.day == 8 else 0)
    daily['is_jewish_holiday'] = pd.to_datetime(daily['date']).isin(israel_holidays).astype(int)
    daily['is_holiday'] = (
        (daily['is_christmas'] == 1) |
        (daily['is_valentines'] == 1) |
        (daily['is_womens_day'] == 1) |
        (daily['is_jewish_holiday'] == 1)
    ).astype(int)

    # 4. אימון מודל
    X = daily[['day_of_week', 'day_of_month', 'month', 'is_weekend', 'is_start_of_month', 'is_end_of_month', 'is_holiday']]
    y = daily['transaction_count']
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    model = XGBRegressor(objective='reg:squarederror', n_estimators=100, random_state=42)
    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)
    print(f"🔍 MSE: {mean_squared_error(y_test, y_pred):.2f}")
    print(f"📈 R²: {r2_score(y_test, y_pred):.2f}")

    # 5. בניית תחזית (שבועי או חודשי)
    if time_range == "weekly":
        forecast_days = pd.date_range(start=datetime.now().date(), periods=7)
    elif time_range == "monthly":
        forecast_days = pd.date_range(start=datetime.now().date(), periods=30)
    else:
        raise ValueError("Invalid time_range. Use 'weekly' or 'monthly'")

    forecast_df = pd.DataFrame({
        'date': forecast_days,
        'day_of_week': forecast_days.dayofweek.map(lambda x: 1 if x == 6 else x + 2),
        'day_of_month': forecast_days.day,
        'month': forecast_days.month,
    })
    forecast_df['is_weekend'] = forecast_df['day_of_week'].isin([6, 7]).astype(int)
    forecast_df['is_start_of_month'] = (forecast_df['day_of_month'] <= 3).astype(int)
    forecast_df['is_end_of_month'] = (forecast_df['day_of_month'] >= 28).astype(int)
    forecast_df['is_christmas'] = forecast_df['date'].apply(lambda d: 1 if d.month == 12 and d.day == 25 else 0)
    forecast_df['is_valentines'] = forecast_df['date'].apply(lambda d: 1 if d.month == 2 and d.day == 14 else 0)
    forecast_df['is_womens_day'] = forecast_df['date'].apply(lambda d: 1 if d.month == 3 and d.day == 8 else 0)
    forecast_df['is_jewish_holiday'] = pd.to_datetime(forecast_df['date']).isin(israel_holidays).astype(int)
    forecast_df['is_holiday'] = (
        (forecast_df['is_christmas'] == 1) |
        (forecast_df['is_valentines'] == 1) |
        (forecast_df['is_womens_day'] == 1) |
        (forecast_df['is_jewish_holiday'] == 1)
    ).astype(int)

    forecast_df['predicted_transactions'] = model.predict(forecast_df[X.columns])
    forecast_df['smb_id'] = smb_id

    json_str = forecast_df[['smb_id', 'date', 'predicted_transactions']].to_json(orient='records', date_format='iso')
    return json.loads(json_str)

