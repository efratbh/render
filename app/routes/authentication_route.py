from flask import Blueprint, jsonify, request
from app.service.authentication_service import check_if_password_correct


auth_blueprint = Blueprint('authentication', __name__)

@auth_blueprint.route('/', methods=['POST'])
def authentication_route():
    try:
        data = request.get_json()
        owner_full_name = data.get('owner_full_name')
        password = data.get('password')

        if not owner_full_name or not password:
            return jsonify({"message": "Missing required fields"}), 400

        results: dict = check_if_password_correct(owner_full_name=owner_full_name,
                                                              password=password)
        if results['is_password_correct']:
            return jsonify(results), 200

        return jsonify({"is_password_correct": results['is_password_correct']}), 401

    except Exception as e:
        return jsonify({'Message': f'Something got wrong, please try again. Error: {str(e)}'}), 500
