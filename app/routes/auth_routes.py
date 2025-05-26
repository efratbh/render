from flask import Blueprint, jsonify

from app.service.authentication_service import check_if_password_correct


auth_blueprint = Blueprint('authentication', __name__)

@auth_blueprint.route('/<string:owner_full_name>/<string:password>', methods=['GET'])
def authentication_route(owner_full_name: str, password: str):
    try:
        is_password_correct: bool = check_if_password_correct(owner_full_name=owner_full_name,
                                                              password=password)
        print(owner_full_name, password)
        return jsonify({"is_password_correct": is_password_correct}), 200

    except Exception as e:
        return jsonify({'Message': 'Error, Something got wrong, please try again'}), 500
