import os
from flask_appbuilder.security.manager import AUTH_DB

basedir = os.path.abspath(os.path.dirname(__file__))

CSRF_ENABLED = True
SECRET_KEY = '\2\1thisismyscretkey\1\2\e\y\y\h'

SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
SQLALCHEMY_TRACK_MODIFICATIONS = False

AUTH_TYPE = AUTH_DB
AUTH_USER_REGISTRATION = True
AUTH_USER_REGISTRATION_ROLE = 'Public'

FAB_API_SWAGGER_UI = True