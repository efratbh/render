from flask_restx import Namespace, Resource, fields
from flask import request
from app.service.authentication_service import check_if_password_correct

auth_ns = Namespace('Authentication', description='User authentication operations')

auth_model = auth_ns.model('AuthInput', {
    'owner_full_name': fields.String(required=True, description='Owner full name'),
    'password': fields.String(required=True, description='Password'),
})

@auth_ns.route('/')
class AuthenticationRoute(Resource):
    @auth_ns.expect(auth_model)
    def post(self):
        data = request.get_json()
        owner_full_name = data.get('owner_full_name')
        password = data.get('password')

        if not owner_full_name or not password:
            return {"message": "Missing required fields"}, 400

        results = check_if_password_correct(owner_full_name=owner_full_name, password=password)

        if results.get('is_password_correct'):
            return results, 200

        return {"is_password_correct": False}, 401
