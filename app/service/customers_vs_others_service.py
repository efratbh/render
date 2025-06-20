from app.sql_db.repository.category_repository import get_category_id
from app.sql_db.repository.transactions_repository import get_my_customers_count, get_similar_customers_avg
from app.utils.date_ranges_utils import get_all_valid_weeks, get_all_month_ranges


def weekly_customers_comparison(smb_id):
    return compare_customers(smb_id, get_all_valid_weeks())

def monthly_customers_comparison(smb_id):
    return compare_customers(smb_id, get_all_month_ranges())

def compare_customers(smb_id, ranges):
    results = []

    category_id = get_category_id(smb_id)
    if not category_id:
        return [{"error": f"לא נמצאה קטגוריה לעסק {smb_id}"}]

    for start, end in ranges:
        results.append({
            "start_date": start.isoformat(),
            "end_date": end.isoformat(),
            "my_customers_count": round(get_my_customers_count(smb_id, start, end), 1),
            "similar_avg_customers_count": get_similar_customers_avg(category_id, smb_id, start, end)
        })

    return results