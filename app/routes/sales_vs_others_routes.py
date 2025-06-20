from flask import Blueprint, jsonify
from app.service.sales_vs_others_service import weekly_sales_comparison, monthly_sales_comparison


compare_sales_blueprint = Blueprint('compare_sales', __name__)


@compare_sales_blueprint.route('/monthly/<int:smb_id>', methods=['GET'])
def compare_sales_monthly_route(smb_id: int):
    try:
        compare_sales_monthly_details: list[dict] = monthly_sales_comparison(smb_id=smb_id)

        if compare_sales_monthly_details:
            return jsonify(compare_sales_monthly_details), 200

        return jsonify({"Message": 'Bad'}), 400

    except Exception as e:
        print(str(e))
        return jsonify({'Message': 'Error, Something got wrong, please try again'}), 500

@compare_sales_blueprint.route('/weekly/<int:smb_id>', methods=['GET'])
def compare_sales_weekly_route(smb_id: int):
    try:
        compare_sales_weekly_details: list[dict] = weekly_sales_comparison(smb_id=smb_id)

        if compare_sales_weekly_details:
            return jsonify(compare_sales_weekly_details), 200

        return jsonify({"Message": 'Bad'}), 400

    except Exception as e:
        print(str(e))
        return jsonify({'Message': 'Error, Something got wrong, please try again'}), 500
