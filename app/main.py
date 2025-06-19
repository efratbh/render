# קובץ מרכזי דרכו נפעיל את האפליקציה
#--------------------
#from flask import Flask

#from app.routes.auth_routes import auth_blueprint
#from app.sql_db.database import init_db

#app = Flask(__name__)

#app.register_blueprint(auth_blueprint, url_prefix='/api/auth')

#if __name__ == '__main__':
 #   init_db()
  #  app.run(port=8080, host='0.0.0.0')

# from GPT
from flask import Flask

from app.routes.compare_customers_routes import compare_blueprint
from app.routes.new_customers_analyzes_routes import new_customers_blueprint
from app.routes.authentication_route import auth_blueprint
from app.routes.sales_vs_past_analyzes_routes import sales_blueprint
from app.sql_db.database import init_db

app = Flask(__name__)#שיהיה מסוגל לתקשר עם API

app.register_blueprint(auth_blueprint, url_prefix='/api/auth')
app.register_blueprint(new_customers_blueprint, url_prefix='/api/analyze/new_customers')
app.register_blueprint(sales_blueprint, url_prefix='/api/analyze/sales')
app.register_blueprint(compare_blueprint, url_prefix='/api/analyze/compare')

# תמיד נריץ את זה, גם ברנדר:
init_db()

if __name__ == '__main__':
    app.run(port=8080, host='0.0.0.0')
