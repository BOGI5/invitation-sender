from app import db


class Organizer:
    __tablename__ = 'organizers'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_name = db.Column(db.String(80), nullable=False)
    last_name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(80), nullable=False, unique=True)

    def __repr__(self):
        return f'<Organizer(name={self.first_name + ' ' + self.last_name}, email={self.email}'


class Event(db.Model):
    __tablename__ = 'events'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50), nullable=False)
    date = db.Column(db.DateTime, nullable=False)
    address = db.Column(db.String(250), nullable=False)
    organizer_id = db.Column(db.Integer, db.ForeignKey('organizers'))

    def __repr__(self):
        return f"<Event(name='{self.name}', date='{self.date}"


class Invitation(db.Model):
    __tablename__ = 'invitations'
    id = db.Column(db, primary_key=True, autoincrement=True)
    event_id = db.Column(db.Integer, db.ForeignKey('events.id'), nullable=False)
    recipient_names = db.Column(db.String(80), nullable=False)
    recipient_email = db.Column(db.String(80), nullable=False)
    replied = db.Column(db.Boolean, nullable=False, default=False)
    attendance = db.Column(db.Boolean, nullable=False, default=False)

    def __repr__(self):
        return f"<Invitation(recipient='{self.recipient_names}', replied='{self.replied}, attendance='{self.attendance}')>"

