from flask_restx import Namespace, Resource
from app.service.customers_vs_others_service import (
    monthly_customers_comparison,
    weekly_customers_comparison
)

customers_vs_others_ns = Namespace('Compare Customers', description='Compare customer counts vs other businesses')

@customers_vs_others_ns.route('/monthly/<int:smb_id>')
class CompareCustomersMonthly(Resource):
    def get(self, smb_id: int):
        try:
            result = monthly_customers_comparison(smb_id=smb_id)
            if result:
                return result, 200
            return {"message": "No data found"}, 400
        except Exception as e:
            return {"message": f"Server error: {str(e)}"}, 500


@customers_vs_others_ns.route('/weekly/<int:smb_id>')
class CompareCustomersWeekly(Resource):
    def get(self, smb_id: int):
        try:
            result = weekly_customers_comparison(smb_id=smb_id)
            if result:
                return result, 200
            return {"message": "No data found"}, 400
        except Exception as e:
            return {"message": f"Server error: {str(e)}"}, 500
