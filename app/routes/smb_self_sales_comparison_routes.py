from flask_restx import Namespace, Resource
from datetime import datetime
from zoneinfo import ZoneInfo
from app.service.smb_self_sales_comparison_service import (
    get_weekly_sales_comparison_json,
    get_weekly_sales_per_month_comparison_json,
    get_yearly_sales_comparison_json
)

self_sales_ns = Namespace(
    'Self Sales Analysis',
    description='Analyze the business’s own sales performance over different periods'
)


@self_sales_ns.route('/weekly/<int:smb_id>')
class WeeklySales(Resource):
    def get(self, smb_id):
        end_date = datetime(2023, 5, 1, tzinfo=ZoneInfo("Asia/Jerusalem"))
        try:
            result = get_weekly_sales_comparison_json(smb_id=smb_id, end_date=end_date)
            if result:
                return result, 200
            return {"message": f"There is no data about this smb_id: {smb_id}"}, 400
        except Exception:
            return {"error": "Something went wrong, please try again"}, 500


@self_sales_ns.route('/monthly/<int:smb_id>')
class MonthlySales(Resource):
    def get(self, smb_id):
        try:
            result = get_weekly_sales_per_month_comparison_json(smb_id=smb_id)
            if result:
                return result, 200
            return {"message": f"There is no data about this smb_id: {smb_id}"}, 400
        except Exception:
            return {"error": "Something went wrong, please try again"}, 500


@self_sales_ns.route('/yearly/<int:smb_id>')
class YearlySales(Resource):
    def get(self, smb_id):
        try:
            result = get_yearly_sales_comparison_json(smb_id=smb_id)
            if result:
                return result, 200
            return {"message": f"There is no data about this smb_id: {smb_id}"}, 400
        except Exception:
            return {"error": "Something went wrong, please try again"}, 500
