from flask import Flask
from flaskext.mysql import MySQL
# from flask_mysqldb import MySQL 
import mysql.connector
import pymysql
from flask_sqlalchemy import SQLAlchemy, sqlalchemy
from flask_login import LoginManager

db = SQLAlchemy()
mysql = MySQL()
ADMIN = 'admin'
PASSWORD = '12345678'
UPLOAD_FOLDER = '/uploads/'
def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'first_flask_app'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+pymysql://{ADMIN}:{PASSWORD}@database-1.chtgj6aaxsxv.us-east-2.rds.amazonaws.com:3306/users?charset=utf8'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['MYSQL_DATABASE_HOST'] = 'database-1.chtgj6aaxsxv.us-east-2.rds.amazonaws.com'
    app.config['MYSQL_DATABASE_PORT'] = 3306
    app.config['MYSQL_DATABASE_USER'] = 'admin'
    app.config['MYSQL_DATABASE_PASSWORD'] = '12345678'
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    

    from .models import User, Recipients, Billing

    mysql.init_app(app)
    init_db(app)
    db.init_app(app)
    db.create_all(app=app)
    clean_db(app, User, Recipients, Billing)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    return app


def init_db(app):
    with app.app_context():
        cursor = mysql.get_db().cursor()

        try:
            print('Trying to create a users table.')
            cursor.execute('''CREATE DATABASE users''')
        except pymysql.err.ProgrammingError:
            print('A user table already exists.')

        cursor.execute("SHOW DATABASES")

        for database in cursor:
            print(database)


def clean_db(app, User, Recipients, Billing):
    with app.app_context():
        db.session.query(User).delete()
        db.session.commit()

        db.session.query(Recipients).delete()
        db.session.commit()

        db.session.query(Billing).delete()
        db.session.commit()

# def populate_table(app, User):
#     db.create_all(app=app)
