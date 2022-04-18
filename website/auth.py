import logging
import os
from datetime import datetime, timedelta
from functools import wraps

import jwt
from flask import Blueprint, request, g, abort, jsonify
from flask import current_app as app

from .models import User
from .shared import db

auth = Blueprint('auth', __name__)


def decode_cookie():
    cookie = request.cookies.get('user')
    if not cookie:
        g.cookie = {}
        return

    try:
        g.cookie = jwt.decode(cookie, os.environ['SECRET_KEY'], algorithms=["HS256"])
    except jwt.InvalidTokenError as err:
        logging.warning(str(err))
        abort(401)


def token_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        token = None
        if 'x-access-tokens' in request.headers:
            token = request.headers['x-access-tokens']

        if not token:
            return jsonify({'message': 'a valid token is missing'})
        try:
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])
            current_user = User.query.filter_by(public_id=data['public_id']).first()
        except jwt.ExpiredSignatureError:
            return jsonify({'message': 'token is expired, log in again'})
        except jwt.InvalidTokenError:
            return jsonify({'message': 'token is invalid'})
        return func(current_user, *args, **kwargs)

    return wrapper


@auth.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    user = User.query.filter_by(username=username).first()
    if user:
        if user.verify_password(password):
            token = jwt.encode({
                'public_id': user.public_id,
                'exp': datetime.utcnow() + timedelta(minutes=45),
            }, app.config["SECRET_KEY"], algorithm="HS256")
            return jsonify({'token': token})
        else:
            abort(404, 'Wrong password')
    else:
        abort(404, "User does not exist")


@auth.route('/logout')
@token_required
def logout():
    # TODO add token to blacklist on logout
    return ''


@auth.route('/sign-up', methods=['POST'])
def sign_up():
    data = request.get_json()
    username = data['username']
    email = data['email']
    password = data['password']

    user_with_email = User.query.filter_by(email=email).first()
    user_with_username = User.query.filter_by(email=email).first()
    if user_with_email:
        abort(400, 'This email address is already in use')
    if user_with_username:
        abort(400, 'This username is already in use')

    new_user = User()
    new_user.email = email
    new_user.username = username
    new_user.password = password
    new_user.last_login = datetime.now()

    db.session.add(new_user)
    db.session.commit()

    token = jwt.encode({
        'public_id': new_user.public_id,
        'exp': datetime.utcnow() + timedelta(minutes=45),
    }, app.config["SECRET_KEY"], algorithm="HS256")
    return jsonify({'token': token})
