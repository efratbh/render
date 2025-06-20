from flask import Blueprint, jsonify

from app.service.customers_vs_others_service import monthly_customers_comparison, \
    weekly_customers_comparison


compare_customers_blueprint = Blueprint('compare_customers', __name__)


@compare_customers_blueprint.route('/monthly/<int:smb_id>', methods=['GET'])
def compare_customers_monthly_route(smb_id: int):
    try:
        compare_customers_monthly_details: list[dict] = monthly_customers_comparison(smb_id=smb_id)

        if compare_customers_monthly_details:
            return jsonify(compare_customers_monthly_details), 200

        return jsonify({"Message": 'Bad'}), 400

    except Exception as e:
        print(str(e))
        return jsonify({'Message': 'Error, Something got wrong, please try again'}), 500

@compare_customers_blueprint.route('/weekly/<int:smb_id>', methods=['GET'])
def compare_customers_weekly_route(smb_id: int):
    try:
        compare_customers_weekly_details: list[dict] = weekly_customers_comparison(smb_id=smb_id)

        if compare_customers_weekly_details:
            return jsonify(compare_customers_weekly_details), 200

        return jsonify({"Message": 'Bad'}), 400

    except Exception as e:
        print(str(e))
        return jsonify({'Message': 'Error, Something got wrong, please try again'}), 500
