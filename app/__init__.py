from time import sleep
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
from flask_login import LoginManager
from config import Config

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
mail = Mail(app)
loginManager = LoginManager(app)
loginManager.init_app(app)

from app import model, view, controller

sleep(5)
with app.app_context():
    db.drop_all()
    db.create_all()
