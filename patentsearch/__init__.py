import os
import sys

from logging import DEBUG
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

basedir = os.path.abspath(os.path.dirname(__file__))

#setting up configuration
app = Flask(__name__)
app.config['SECRET_KEY'] = '~t\x86\xc9\x1ew\x8bOcX\x85O\xb6\xa2\x11kL\xd1\xce\x7f\x14<y\x9e'
sql_location = os.path.join(basedir, 'App_Data')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(sql_location, 'patentsearch.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['DEBUG'] = False
db = SQLAlchemy(app)

#Flask-Login provides user session management for Flask
login_manager = LoginManager()
login_manager.session_protection = "strong"
login_manager.login_view = "login"
login_manager.init_app(app)

import patentsearch.models
import patentsearch.views



