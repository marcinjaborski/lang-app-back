import os

from flask import Flask
from flask_cors import CORS

from .auth import decode_cookie
from .models import User, Note
from .shared import db


def create_app():
    app = Flask(__name__)
    CORS(app)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:admin@localhost/noteo_dev'
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    os.environ['SECRET_KEY'] = 'rwegagewagaweqgwearggr'
    app.secret_key = os.environ['SECRET_KEY']
    db.init_app(app)
    app.before_request_funcs.setdefault(None, [decode_cookie])

    from .auth import auth
    from .controllers import controllers

    app.register_blueprint(auth, url_prefix='/')
    app.register_blueprint(controllers, url_prefix='/')

    return app
