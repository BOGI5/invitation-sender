from app import app, loginManager, mail
from app.model import *
from flask import redirect, url_for
from flask_login import login_user, logout_user, current_user
from flask_mail import Message
from sqlalchemy.exc import IntegrityError


@loginManager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


def create_user(request):
    try:
        user = User(request.form['first_name'], request.form['last_name'], request.form['email'], request.form['password'])
        db.session.add(user)
        db.session.commit()
        login_user(user)
        return 0
    except IntegrityError:
        db.session.rollback()
        return 1


def validate_user(request):
    user = User.query.filter_by(email=request.form['email']).first()
    if not user:
        return 1
    if user.password == request.form['password']:
        login_user(user)
        return 0
    else:
        return 2


def get_users():
    return User.query.all()


@app.route('/logout')
def logout():
    logout_user()
    return redirect('/')


@app.route('/delete_user')
def delete_user():
    delete_all_events(current_user.id)
    db.session.delete(current_user)
    db.session.commit()
    return redirect('/logout')


@app.route('/delete_event/<int:event_id>')
def delete_event(event_id):
    event = Event.query.filter_by(id=event_id).first()
    delete_all_invitations(event_id)
    db.session.delete(event)
    db.session.commit()
    return redirect(f"/view_events/{event.user_id}")


def delete_all_events(user_id):
    events = Event.query.filter_by(user_id=user_id).all()
    for event in events:
        delete_all_invitations(event.id)
        db.session.delete(event)
    db.session.commit()


def delete_all_invitations(event_id):
    invitations = Invitation.query.filter_by(event_id=event_id).all()
    for invitation in invitations:
        db.session.delete(invitation)
    db.session.commit()


def add_event(request, user_id):
    event = Event(name=request.form['name'], date=request.form['date'], address=request.form['address'],
                  user_id=user_id)
    db.session.add(event)
    db.session.commit()
    return event.id


def get_event(event_id):
    return Event.query.filter_by(id=event_id).first()


def get_events(user_id):
    return Event.query.filter_by(user_id=user_id).all()


def get_invitations(event_id):
    return Invitation.query.filter_by(event_id=event_id).all()


def add_invitation(request, event_id):
    try:
        invitation = Invitation(event_id=event_id,
                            recipient_email=request.form['email'], recipient_names=request.form['names'])
        db.session.add(invitation)
        db.session.commit()
        send_invitation(invitation)
        return invitation.id
    except IntegrityError:
        db.session.rollback()
        return -1


@app.route('/delete_invitation/<int:invitation_id>')
def delete_invitation(invitation_id):
    invitation = Invitation.query.filter_by(id=invitation_id).first()
    db.session.delete(invitation)
    db.session.commit()
    return redirect(f"/show_invitations/{invitation.event_id}")


def send_invitation(invitation):
    message = Message(subject="Invitation", recipients=[invitation.recipient_email])
    message.body = str(invitation.recipient_names + ",\n" + "You're invited!" + " Please go to the " +
                 url_for('reply_invitation', invitation_id=invitation.id, _external=True) +
                 " to confirm your attendance on this event.\nYour pin: " + invitation.pin)
    mail.send(message)


def get_invitation(invitation_id):
    return Invitation.query.filter_by(id=invitation_id).first()


def answer_invitation(invitation_id, reply, pin):
    invitation = get_invitation(invitation_id)
    if invitation is None:
        return "This invitation does not exists!"
    if invitation.pin == pin:
        invitation.replied = True
        invitation.attendance = reply
        db.session.commit()
        return "Thank you for your reply! You can close this window."
    return "Wrong PIN! Your reply is not registered! "
