from app.sql_db.repository.category_repository import get_category_id
from app.sql_db.repository.transactions_repository import get_my_transaction_total, get_similar_transaction_avg
from app.utils.date_ranges_utils import get_all_valid_weeks, get_all_month_ranges


def weekly_sales_comparison(smb_id):
    return compare_sales(smb_id, get_all_valid_weeks())

def monthly_sales_comparison(smb_id):
    return compare_sales(smb_id, get_all_month_ranges())

def compare_sales(smb_id, ranges):
    results = []

    category_id = get_category_id(smb_id)
    if not category_id:
        return [{"error": f"לא נמצאה קטגוריה לעסק {smb_id}"}]

    for start, end in ranges:
        results.append({
            "start_date": start.isoformat(),
            "end_date": end.isoformat(),
            "my_total_transaction_amount": float((get_my_transaction_total(smb_id=smb_id, start_date=start, end_date= end)) or 0),
            "similar_avg_transaction_amount": float((get_similar_transaction_avg(category_id=category_id, smb_id=smb_id,
                                                                          start_date=start, end_date=end)) or 0)
        })

    return results
