from flask import Flask
from app.routes.init_routes import register_all_blueprints
from app.sql_db.database import init_db


app = Flask(__name__)
register_all_blueprints(app)
init_db()

if __name__ == '__main__':
    app.run(port=8080, host='0.0.0.0')
