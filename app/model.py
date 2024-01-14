from app import db
from flask_login import UserMixin


class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_name = db.Column(db.String(80), nullable=False)
    last_name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(80), nullable=False, unique=True)
    password = db.Column(db.String(80), nullable=False)

    def __init__(self, first_name, last_name, email, password):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.password = password

    def __repr__(self):
        return f"<User(name={self.first_name + ' ' + self.last_name}, email={self.email}"


class Event(db.Model):
    __tablename__ = 'events'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50), nullable=False)
    date = db.Column(db.DateTime, nullable=False)
    address = db.Column(db.String(250), nullable=False)
    organizer_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    def __init__(self, name, date, address, organizer_id):
        self.name = name
        self.date = date
        self.address = address
        self.organizer = organizer_id

    def __repr__(self):
        return f"<Event(name='{self.name}', date='{self.date}"


class Invitation(db.Model):
    __tablename__ = 'invitations'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    event_id = db.Column(db.Integer, db.ForeignKey('events.id'), nullable=False)
    recipient_names = db.Column(db.String(80), nullable=False)
    recipient_email = db.Column(db.String(80), nullable=False)
    replied = db.Column(db.Boolean, nullable=False, default=False)
    attendance = db.Column(db.Boolean, nullable=False, default=False)

    def __init__(self, event_id, recipient_names, recipient_email):
        self.event_id = event_id
        self.recipient_names = recipient_names
        self.recipient_email = recipient_email

    def __repr__(self):
        return f"<Invitation(recipient='{self.recipient_names}', replied='{self.replied}, attendance='{self.attendance}')>"
