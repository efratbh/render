from flask_restx import Namespace, Resource
from app.service.sales_vs_others_service import (
    weekly_sales_comparison,
    monthly_sales_comparison
)

sales_vs_others_ns = Namespace(
    'Sales Comparison',
    description='Compare sales between the target business and similar businesses'
)

@sales_vs_others_ns.route('/monthly/<int:smb_id>')
class SalesMonthlyComparison(Resource):
    def get(self, smb_id: int):
        try:
            result = monthly_sales_comparison(smb_id=smb_id)
            print(result)
            if result:
                return result, 200
            return {"message": "No data found"}, 400
        except Exception as e:
            return {"message": f"Server error: {str(e)}"}, 500


@sales_vs_others_ns.route('/weekly/<int:smb_id>')
class SalesWeeklyComparison(Resource):
    def get(self, smb_id: int):
        try:
            result = weekly_sales_comparison(smb_id=smb_id)
            if result:
                return result, 200
            return {"message": "No data found"}, 400
        except Exception as e:
            return {"message": f"Server error: {str(e)}"}, 500
