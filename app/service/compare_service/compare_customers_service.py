from app.sql_db.repository.sa import compare_customers, monthly_customers_comparison, weekly_customers_comparison


def weekly_customers_comparison_se(smb_id: int):
    customers_weekly_details: dict = weekly_customers_comparison(smb_id)
    return customers_weekly_details

def monthly_customers_comparison_se(smb_id: int):
    customers_monthly_details: dict = monthly_customers_comparison(smb_id)
    return customers_monthly_details
