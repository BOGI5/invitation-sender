from flask import request, render_template, url_for, redirect, jsonify
from app import app
from app.model import *


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/show_organizer')
def show_organizer():
    return jsonify(invitation=Organizer.query.all())


@app.route('/create_organizer', methods=['POST', 'GET'])
def create_organizer():
    if request.method == 'POST':
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        email = request.form['email']
        organizer = Organizer(first_name=first_name, last_name=last_name, email=email)
        db.session.add(organizer)
        db.session.commit()
        return redirect(url_for('show_organizer'))
    elif request.method == 'GET':
        return render_template('create_organizer.html')
