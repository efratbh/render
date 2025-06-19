from flask import Blueprint, jsonify
from datetime import datetime
from zoneinfo import ZoneInfo
from app.sql_db.database import session_maker
from app.sql_db.repository.ba import get_weekly_sales_comparison_json, get_weekly_sales_per_month_comparison_json, \
    get_yearly_sales_comparison_json


sales_blueprint = Blueprint('sales', __name__)


@sales_blueprint.route('/weekly/<int:smb_id>', methods=['GET'])
def weekly_sales_route(smb_id):
    end_date = datetime(2023, 5, 1, tzinfo=ZoneInfo("Asia/Jerusalem"))
    with session_maker() as session:
        try:
            result = get_weekly_sales_comparison_json(session, smb_id, end_date)
            if result:
                return jsonify(result), 200
            return jsonify({f'Message': f'There is not data about this smb_id: {smb_id}'}), 400
        except Exception as e:
            return jsonify({'Error': 'Something got wrong, please try again'}), 500

@sales_blueprint.route('/monthly/<int:smb_id>', methods=['GET'])
def monthly_sales_route(smb_id):
    with session_maker() as session:
        try:
            result = get_weekly_sales_per_month_comparison_json(session, smb_id)
            if result:
                return jsonify(result), 200
            return jsonify({f'Message': f'There is not data about this smb_id: {smb_id}'}), 400
        except Exception as e:
            return jsonify({'Error': 'Something got wrong, please try again'}), 500

@sales_blueprint.route('/yearly/<int:smb_id>', methods=['GET'])
def yearly_sales_route(smb_id):
    with session_maker() as session:
        try:
            result = get_yearly_sales_comparison_json(session, smb_id)
            if result:
                return jsonify(result), 200
            return jsonify({f'Message': f'There is not data about this smb_id: {smb_id}'}), 400
        except Exception as e:
            return jsonify({'Error': 'Something got wrong, please try again'}), 500
