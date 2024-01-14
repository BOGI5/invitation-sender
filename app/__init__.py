from time import sleep
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
from config import Config
import subprocess

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
mail = Mail(app)

from app import model, view, controller

subprocess.run(["wait-for-it", "--timeout=0", "mysql:3306"])
sleep(5)
