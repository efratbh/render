from flask_restx import Namespace, Resource
from app.service.sales_forecast_service import monthly_sales_forecast, weekly_sales_forcast


sales_forecast_ns = Namespace(
    'Sales Forecast',
    description='Provides endpoints for predicting and analyzing future sales trends based on historical transaction data.'
)

@sales_forecast_ns.route('/monthly/<int:smb_id>')
class SalesMonthlyForcast(Resource):
    def get(self, smb_id: int):
        try:
            result = monthly_sales_forecast(smb_id=smb_id)

            if result:
                return result, 200

            return {"message": "No data found"}, 400

        except Exception as e:
            return {"message": f"Server error: {str(e)}"}, 500


@sales_forecast_ns.route('/weekly/<int:smb_id>')
class SalesWeeklyForecast(Resource):
    def get(self, smb_id: int):
        try:
            result = weekly_sales_forcast(smb_id=smb_id)

            if result:
                return result, 200

            return {"message": "No data found"}, 400

        except Exception as e:
            return {"message": f"Server error: {str(e)}"}, 500
