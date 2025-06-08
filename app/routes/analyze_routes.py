from flask import Blueprint, jsonify

from app.service.new_customers_analyzes import get_monthly_new_customers_analysis


analyzes_blueprint = Blueprint('analyzes', __name__)


@analyzes_blueprint.route('/new_customers/monthly/<int:smb_id>', methods=['GET'])
def new_customers_per_month_route(smb_id: int):
    try:
        new_customers_details: list[dict] = get_monthly_new_customers_analysis(smb_id)

        if new_customers_details:
            return jsonify(new_customers_details), 200

        return jsonify({"Message": 'Baddddddddddddddddddd'}), 400

    except Exception as e:
        print(str(e))
        return jsonify({'Message': 'Error, Something got wrong, please try again'}), 500
