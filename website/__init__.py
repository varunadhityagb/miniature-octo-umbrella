from flask import Flask
from flask_mysqldb import MySQL
import os
from datetime import timedelta
from werkzeug.security import generate_password_hash, check_password_hash


def create_app():
    global mysql
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'fngkfglijheklgdfgu jfnfjghbfdgj'
    app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=1)
    app.config['MYSQL_USER'] = 'root'
    app.config['MYSQL_HOST'] = 'localhost'
    app.config["MYSQL_PASSWORD"] = 'mysql'
    app.config['MYSQL_DB'] = 'project_scam'

    mysql = MySQL(app)

    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix = '/')

    return app


def get_auth_key(dob):
    dob = dob.split('-')
    dob = ''.join(dob)
    return generate_password_hash(dob, method='sha256')


def backup_database():
    os.system("mysqldump -u root -pmysql -d -B --events --routines --triggers project_scam  --add-drop-table --add-locks > website\static\database\project_scam.sql")


backup_database()