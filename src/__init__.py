from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import flask_login
import hashlib
import os


webapp = Flask(__name__)

username = os.getenv('LOGIN', 'admin')
passwd_hash = os.getenv('PASSWD_HASH')
webapp.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

login_manager = flask_login.LoginManager(webapp)
login_manager.login_view = 'login'

webapp.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///../xss.db'
webapp.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
webapp.config['SESSION_COOKIE_SAMESITE'] = 'Lax'

db = SQLAlchemy()
db.init_app(webapp)


class User(flask_login.UserMixin):
    id = username

    @staticmethod
    def check_auth(login, passwd):
        input_hash = hashlib.md5(bytes(passwd, 'UTF8')).hexdigest()
        return login == username and input_hash == passwd_hash


@login_manager.user_loader
def user_loader(login):
    return User()


from src.views import admin
from src.views import callback
from src.views import api
