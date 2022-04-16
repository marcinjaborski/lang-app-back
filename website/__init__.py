from flask import Flask
from flask_login import LoginManager
from flask_cors import CORS
from .models import User
from .shared import db


def create_app():
    app = Flask(__name__)
    CORS(app)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:admin@localhost/noteo_dev'
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.secret_key = 'secret string'
    db.init_app(app)

    from .auth import auth
    from .controllers import controllers

    app.register_blueprint(auth, url_prefix='/')
    app.register_blueprint(controllers, url_prefix='/')

    # db.create_all(app=app)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    return app
