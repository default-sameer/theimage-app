from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_view_counter import ViewCounter

app = Flask(__name__)

app.config.from_object(Config)
db = SQLAlchemy(app)
login = LoginManager(app)
login.login_view = 'login'
login.login_message = ('Log in To access this page')

view_counter = ViewCounter(app, db)

from app import views, models
