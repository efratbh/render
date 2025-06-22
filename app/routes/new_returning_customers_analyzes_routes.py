from flask_restx import Namespace, Resource
from app.service.new_returning_customers_analyzes_service import (
    get_monthly_new_customers_analysis,
    get_weekly_new_customers_analysis
)

new_returning_customers_ns = Namespace('New vs Returning Customers Analysis', description='Analyze new/returning customers over time')

@new_returning_customers_ns.route('/yearly/<int:smb_id>')
class NewCustomersPerMonth(Resource):
    def get(self, smb_id: int):
        try:
            result = get_monthly_new_customers_analysis(smb_id=smb_id)
            if result:
                return result, 200
            return {"message": "No data found"}, 400
        except Exception as e:
            return {"message": f"Server error: {str(e)}"}, 500


@new_returning_customers_ns.route('/monthly/<int:smb_id>')
class NewCustomersPerWeek(Resource):
    def get(self, smb_id: int):
        try:
            result = get_weekly_new_customers_analysis(smb_id=smb_id)
            if result:
                return result, 200
            return {"message": "No data found"}, 400
        except Exception as e:
            return {"message": f"Server error: {str(e)}"}, 500
