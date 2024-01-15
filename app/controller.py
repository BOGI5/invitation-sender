from app import app, loginManager
from app.model import *
from flask import redirect
from flask_login import login_user, logout_user


@loginManager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


def create_user(request):
    user = User(request.form['first_name'], request.form['last_name'], request.form['email'], request.form['password'])
    db.session.add(user)
    db.session.commit()


def validate_user(request):
    user = User.query.filter_by(email=request.form['email']).first()
    if user.password == request.form['password']:
        login_user(user)


def get_users():
    return User.query.all()


@app.route('/logout')
def logout():
    logout_user()
    return redirect('/')


@app.route('/delete_event/<int:event_id>')
def delete_event(event_id):
    event = Event.query.filter_by(id=event_id).first()
    db.session.delete(event)
    db.session.commit()
    return redirect('/user_information')


def add_event(request, user_id):
    event = Event(name=request.form['name'], date=request.form['date'], address=request.form['address'],
                  user_id=user_id)
    db.session.add(event)
    db.session.commit()


def get_event(event_id):
    return Event.query.filter_by(id=event_id).first()


def get_events(user_id):
    return Event.query.filter_by(user_id=user_id).all()
