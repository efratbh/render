from flask_restx import Api

from app.routes.authentication_route import auth_ns
from app.routes.customers_vs_others_routes import customers_vs_others_ns
from app.routes.new_returning_customers_analyzes_routes import new_returning_customers_ns
from app.routes.recommendations_vs_others_routes import recommendations_vs_others_ns
from app.routes.sales_forecast_routes import sales_forecast_ns
from app.routes.sales_vs_others_routes import sales_vs_others_ns
from app.routes.smb_self_sales_comparison_routes import self_sales_ns


def register_all_namespaces(api: Api):
    api.add_namespace(auth_ns, path='/api/auth')
    api.add_namespace(new_returning_customers_ns, path='/api/analyze/new-customers')
    api.add_namespace(self_sales_ns, path='/api/analyze/sales')
    api.add_namespace(customers_vs_others_ns, path='/api/analyze/compare-customers')
    api.add_namespace(sales_vs_others_ns, path='/api/analyze/compare-sales')
    api.add_namespace(recommendations_vs_others_ns, path='/api/analyze/compare-recommendations')
    api.add_namespace(sales_forecast_ns, path='/api/analyze/sales-forecast')
