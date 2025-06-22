from flask import Flask
from flask_restx import Api
from app.routes.api_registry import register_all_namespaces
from app.sql_db.database import init_db

app = Flask(__name__)
api = Api(app, version="1.0", title="LINX BI API", description="Business Intelligence API")

register_all_namespaces(api)
init_db()

if __name__ == '__main__':
    app.run(port=8080, host='0.0.0.0')
