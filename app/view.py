from flask import request, render_template, url_for, redirect, jsonify
from flask_login import login_user, logout_user, current_user
from app import app
from app.model import *


@app.route('/')
@app.route('/home')
def index():
    return render_template('index.html', user=current_user)


@app.route('/show_users')
def show_users():
    return render_template("show_users.html", users=User.query.all(), user=current_user)


@app.route('/sign_up', methods=['POST', 'GET'])
def sign_up():
    if request.method == 'POST':
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        email = request.form['email']
        password = request.form['password']
        user = User(first_name=first_name, last_name=last_name, email=email, password=password)
        db.session.add(user)
        db.session.commit()
        return redirect('/show_users')
    elif request.method == 'GET':
        return render_template('sign_up.html', user=current_user)


@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        user = User.query.filter_by(email=request.form['email']).first()
        if user.password == request.form['password']:
            login_user(user)
            return redirect('/')
    elif request.method == 'GET':
        return render_template('login.html', user=current_user)


@app.route('/logout')
def logout():
    logout_user()
    return redirect('/')


@app.route('/user_information')
def user_information():
    return render_template('user_information.html', user=current_user)


@app.route('/create_event/<int:user_id>')
def create_event(user_id):
    return redirect('/')
