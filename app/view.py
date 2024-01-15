from flask import request, render_template, url_for, redirect
from flask_login import logout_user, current_user
from app.controller import *


@app.route('/')
@app.route('/home')
def index():
    return render_template('index.html', user=current_user)


@app.route('/show_users')
def show_users():
    return render_template("show_users.html", users=get_users(), user=current_user)


@app.route('/sign_up', methods=['POST', 'GET'])
def sign_up():
    if request.method == 'POST':
        create_user(request)
        return redirect('/user_information')
    elif request.method == 'GET':
        return render_template('sign_up.html', user=current_user)


@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        validate_user(request)
        return redirect('/')
    elif request.method == 'GET':
        return render_template('login.html', user=current_user)


@app.route('/user_information')
def user_information():
    return render_template('user_information.html', user=current_user)


@app.route('/create_event/<int:user_id>', methods=['GET', 'POST'])
def create_event(user_id):
    if request.method == 'POST':
        add_event(request, user_id)
        return redirect('/user_information')
    elif request.method == 'GET':
        return render_template('create_event.html', user=current_user)


@app.route('/view_event/<int:event_id>')
def view_event(event_id):
    return render_template('view_events.html', events=get_event(event_id), user=current_user)


@app.route('/view_events/<int:user_id>')
def show_events(user_id):
    return render_template('view_events.html', events=get_events(user_id), user=current_user)
