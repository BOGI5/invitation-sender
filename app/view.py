from flask import request, render_template, redirect
from flask_login import current_user
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
        return redirect(f"/show_invitations/{add_event(request, user_id)}")
    elif request.method == 'GET':
        return render_template('create_event.html', user=current_user)


@app.route('/view_event/<int:event_id>')
def view_event(event_id):
    return render_template('view_events.html', events=get_event(event_id), user=current_user)


@app.route('/view_events/<int:user_id>')
def show_events(user_id):
    return render_template('view_events.html', events=get_events(user_id), user=current_user)


@app.route('/show_invitations/<int:event_id>')
def show_invitations(event_id):
    return render_template('show_invitations.html', invitations=get_invitations(event_id),
                           user=current_user, event_id=event_id)


@app.route('/create_invitation/<int:event_id>', methods=['GET', 'POST'])
def create_invitation(event_id):
    if request.method == 'POST':
        add_invitation(request, event_id)
        return redirect(f"/show_invitations/{event_id}")
    elif request.method == 'GET':
        return render_template('create_invitation.html', user=current_user)


@app.route('/reply_invitation/<int:invitation_id>', methods=['GET', 'POST'])
def reply_invitation(invitation_id):
    if get_invitation(invitation_id) is None:
        return "This invitation does not exists!"
    if request.method == 'POST':
        reply = request.form['reply']
        if reply == 'yes':
            return answer_invitation(invitation_id, True, str(request.form['pin']))
        elif reply == 'no':
            return answer_invitation(invitation_id, False, str(request.form['pin']))
    elif request.method == 'GET':
        if get_invitation(invitation_id).replied:
            return "Thank you for your reply! You can close this window."
        else:
            return render_template('reply_invitation.html', user=current_user,
                               event=get_event(get_invitation(invitation_id).event_id))
