from flask import Blueprint, jsonify
from app.service.recommendations_vs_others_service import weekly_recommendations_comparison, \
    monthly_recommendations_comparison


compare_recommendations_blueprint = Blueprint('compare_recommendations', __name__)


@compare_recommendations_blueprint.route('/monthly/<int:smb_id>', methods=['GET'])
def compare_recommendations_monthly_route(smb_id: int):
    try:
        compare_recommendations_monthly_details: list[dict] = monthly_recommendations_comparison(smb_id)

        if compare_recommendations_monthly_details:
            return jsonify(compare_recommendations_monthly_details), 200

        return jsonify({"Message": 'Bad'}), 400

    except Exception as e:
        print(str(e))
        return jsonify({'Message': 'Error, Something got wrong, please try again'}), 500

@compare_recommendations_blueprint.route('/weekly/<int:smb_id>', methods=['GET'])
def compare_recommendations_weekly_route(smb_id: int):
    try:
        compare_recommendations_weekly_details: list[dict] = weekly_recommendations_comparison(smb_id=smb_id)

        if compare_recommendations_weekly_details:
            return jsonify(compare_recommendations_weekly_details), 200

        return jsonify({"Message": 'Bad'}), 400

    except Exception as e:
        print(str(e))
        return jsonify({'Message': 'Error, Something got wrong, please try again'}), 500
