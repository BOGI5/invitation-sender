from flask import request, render_template, url_for, redirect, jsonify
from flask_login import login_user, logout_user
from app import app
from app.model import *


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/show_organizer')
def show_organizer():
    return render_template("show_organizers.html", organizers=Organizer.query.all())


@app.route('/sign_up', methods=['POST', 'GET'])
def create_organizer():
    if request.method == 'POST':
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        email = request.form['email']
        password = request.form['password']
        organizer = Organizer(first_name=first_name, last_name=last_name, email=email, password=password)
        db.session.add(organizer)
        db.session.commit()
        return redirect('/show_organizer')
    elif request.method == 'GET':
        return render_template('sign_up.html')


@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        organizer = Organizer.query.filter_by(email=request.form['email']).first()
        if organizer.password == request.form['password']:
            login_user(organizer)
            return redirect('/')
    elif request.method == 'GET':
        return render_template('login.html')


@app.route('/logout')
def logout():
    logout_user()
    return redirect('/')
