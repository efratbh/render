from flask.sansio.app import App

from app.routes.customers_vs_others_routes import compare_customers_blueprint
from app.routes.recommendations_vs_others_routes import compare_recommendations_blueprint
from app.routes.sales_vs_others_routes import compare_sales_blueprint
from app.routes.new_returning_customers_analyzes_routes import new_customers_blueprint
from app.routes.authentication_route import auth_blueprint
from app.routes.smb_self_sales_comparison_routes import sales_blueprint


def register_all_blueprints(app: App):
    app.register_blueprint(auth_blueprint, url_prefix='/api/auth')
    app.register_blueprint(new_customers_blueprint, url_prefix='/api/analyze/new_customers')
    app.register_blueprint(sales_blueprint, url_prefix='/api/analyze/sales')
    app.register_blueprint(compare_customers_blueprint, url_prefix='/api/analyze/compare_customers')
    app.register_blueprint(compare_sales_blueprint, url_prefix='/api/analyze/compare_sales')
    app.register_blueprint(compare_recommendations_blueprint, url_prefix='/api/analyze/compare_recommendations')
