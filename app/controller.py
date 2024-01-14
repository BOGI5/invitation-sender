from app import app
from app.model import *
from app import loginManager


@loginManager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
