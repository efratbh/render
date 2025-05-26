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
from app.routes.auth_routes import auth_blueprint
from app.sql_db.database import init_db

app = Flask(__name__)
app.register_blueprint(auth_blueprint, url_prefix='/api/auth')

# תמיד נריץ את זה, גם ברנדר:
init_db()

if __name__ == '__main__':
    app.run(port=8080, host='0.0.0.0')
