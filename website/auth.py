from flask import Blueprint, request
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from .shared import db
from flask_login import login_user, login_required, logout_user

auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        data = request.get_json()
        username = data['username']
        password = data['password']

        user = User.query.filter_by(username=username).first()
        if user:
            if check_password_hash(user.password, password):
                login_user(user, remember=True)
            else:
                # wrong password
                pass
        else:
            # wrong email
            pass

    return "<p>Login</p>"


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return "<p>Logout</p>"


@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        data = request.get_json()
        username = data['username']
        email = data['email']
        password = data['password']

        user = User.query.filter_by(email=email).first()
        if user:
            # email already exists
            pass

        new_user = User(username=username, email=email, password=generate_password_hash(password, method='sha256'))
        db.session.add(new_user)
        db.session.commit()
        login_user(user, remember=True)
    return "<p>Sign-up</p>"
