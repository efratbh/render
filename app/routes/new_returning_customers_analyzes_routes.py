from flask import Blueprint, jsonify

from app.service.new_returning_customers_analyzes_service import get_monthly_new_customers_analysis, get_weekly_new_customers_analysis


new_customers_blueprint = Blueprint('analyzes', __name__)


@new_customers_blueprint.route('/yearly/<int:smb_id>', methods=['GET'])
def new_customers_per_month_route(smb_id: int):
    try:
        new_customers_monthly_details: list[dict] = get_monthly_new_customers_analysis(smb_id=smb_id)

        if new_customers_monthly_details:
            return jsonify(new_customers_monthly_details), 200

        return jsonify({"Message": 'Bad'}), 400

    except Exception as e:
        print(str(e))
        return jsonify({'Message': f'Error, Something got wrong, please try again. Error: {str(e)}'}), 500

@new_customers_blueprint.route('/monthly/<int:smb_id>', methods=['GET'])
def new_customers_per_week_route(smb_id: int):
    try:
        new_customers_weekly_details: list[dict] = get_weekly_new_customers_analysis(smb_id=smb_id)

        if new_customers_weekly_details:
            return jsonify(new_customers_weekly_details), 200

        return jsonify({"Message": 'Bad'}), 400

    except Exception as e:
        print(str(e))
        return jsonify({'Message': f'Error, Something got wrong, please try again. Error: {str(e)}'}), 500
