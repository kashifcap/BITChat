from time import localtime, strftime
from flask import Flask, render_template, url_for, redirect, flash
import os
from flask_login import LoginManager, login_user, current_user, login_required, logout_user
from wtform_fields import *
from models import *
from flask_socketio import SocketIO, send, emit, join_room, leave_room


app = Flask(__name__)

app.config['WTF_CSRF_SECRET_KEY'] = os.environ.get("WTF_CSRF_SECRET_KEY")
app.config['SECRET_KEY'] = os.environ.get("SECRET_KEY")
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("DATABASE_URI")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

socket_io = SocketIO(app)

ROOMS = ['General','Academic', 'Library', 'Gym', 'Sports', 'Resources', 'Information']

login = LoginManager(app)
login.init_app(app)


@login.user_loader
def load_user(id):
    return User.query.get(int(id))


@app.route("/", methods=['GET', 'POST'])
def index():
    reg_form = RegistrationForm()

    if reg_form.validate_on_submit():
        username = reg_form.username.data
        password = reg_form.password.data

        hashed_pswd = pbkdf2_sha256.hash(password)
        user = User(username=username, password=hashed_pswd)

        db.session.add(user)
        db.session.commit()

        flash("Registered Succesfully. Please login.", 'success')

        return redirect(url_for('login'))

    return render_template("index.html", form=reg_form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    login_form = LoginForm()

    if login_form.validate_on_submit():
        user_object = User.query.filter_by(
            username=login_form.username.data).first()
        login_user(user_object)
        return redirect(url_for('chat'))

    return render_template('login.html', form=login_form)


@app.route("/chat", methods=['GET', 'POST'])
@login_required
def chat():
    return render_template('chat.html', username=current_user.username, rooms=ROOMS)


@app.route("/logout", methods=['GET'])
@login_required
def logout():
    logout_user()
    flash("Logged out successfully", 'success')
    return redirect(url_for('login'))


@socket_io.on('message')
def message(data):
    send({'msg': data['msg'], 'username': data['username'],
          'time_stamp': strftime('%b-%d %I:%M%p', localtime())}, room=data['room'])


@socket_io.on('join')
def join(data):
    join_room(data['room'])
    send({'msg': data['username'] + ' has joined the ' +
          data['room'] + ' room.'}, room=data['room'])


@socket_io.on('leave')
def leave(data):
    leave_room(data['room'])
    send({'msg': data['username'] + ' has left the ' +
          data['room'] + ' room.'}, room=data['room'])


if __name__ == '__main__':
    app.run()
