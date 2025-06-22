from flask_restx import Namespace, Resource
from app.service.recommendations_vs_others_service import (
    weekly_recommendations_comparison,
    monthly_recommendations_comparison
)

recommendations_vs_others_ns = Namespace(
    'Recommendations Comparison',
    description='Compare number of recommendations with other businesses in the same category'
)

@recommendations_vs_others_ns.route('/monthly/<int:smb_id>')
class RecommendationsMonthlyComparison(Resource):
    def get(self, smb_id: int):
        try:
            result = monthly_recommendations_comparison(smb_id)
            if result:
                return result, 200
            return {"message": "No data found"}, 400
        except Exception as e:
            return {"message": f"Server error: {str(e)}"}, 500


@recommendations_vs_others_ns.route('/weekly/<int:smb_id>')
class RecommendationsWeeklyComparison(Resource):
    def get(self, smb_id: int):
        try:
            result = weekly_recommendations_comparison(smb_id=smb_id)
            if result:
                return result, 200
            return {"message": "No data found"}, 400
        except Exception as e:
            return {"message": f"Server error: {str(e)}"}, 500
