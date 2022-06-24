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

    if None in (username, password):
        return {'message': 'Missing arguments'}, 400

    user = User.query.filter_by(username=username).first()
    if not user:
        return {'message': 'User does not exist'}, 404

    if not user.verify_password(password):
        return {'message': 'Wrong password'}, 404

    token = jwt.encode({
        'public_id': user.public_id,
        'exp': datetime.utcnow() + timedelta(minutes=45),
    }, app.config["SECRET_KEY"], algorithm="HS256")
    return {'token': token}


@auth.route('/logout')
@token_required
def logout():
    # TODO add token to blacklist on logout
    return ''


@auth.route('/sign-up', methods=['POST'])
def sign_up():
    data = request.get_json()
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')

    if None in (username, email, password):
        return {'message': 'Missing attributes'}, 400

    user_with_email = User.query.filter_by(email=email).first()
    user_with_username = User.query.filter_by(username=username).first()
    if user_with_email:
        return {'message': 'This email address is already in use'}, 400
    if user_with_username:
        return {'message': 'This username address is already in use'}, 400

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
