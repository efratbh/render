from app.sql_db.repository.category_repository import get_category_id
from app.sql_db.repository.xtribution_repository import get_my_recommendation_count, get_similar_recommendations_avg
from app.utils.date_ranges_utils import get_all_valid_weeks, get_all_month_ranges


def weekly_recommendations_comparison(smb_id):
    return compare_recommendations(smb_id, get_all_valid_weeks())

def monthly_recommendations_comparison(smb_id):
    return compare_recommendations(smb_id, get_all_month_ranges())

def compare_recommendations(smb_id, ranges):
    results = []
    category_id = get_category_id(smb_id)
    if not category_id:
        return [{"error": f"לא נמצאה קטגוריה לעסק {smb_id}"}]
    for start, end in ranges:
        results.append({
            "start_date": start.isoformat(),
            "end_date": end.isoformat(),
            "my_recommendations_count": get_my_recommendation_count(smb_id, start, end),
            "similar_avg_recommendations_count": get_similar_recommendations_avg(category_id, smb_id, start, end)
        })
    return results