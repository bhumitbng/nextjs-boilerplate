from flask import Flask
from flask_appbuilder import AppBuilder, SQLA
from flask_cors import CORS

app = Flask(__name__)
app.config.from_object('config')
db = SQLA(app)
appbuilder = AppBuilder(app, db.session)
CORS(app)

from . import views, models
from .api import meeting_summarizer_api, employee_tracker_api
from .integrations import slack_integration, teams_integration