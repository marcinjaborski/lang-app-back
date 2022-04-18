import uuid
from dataclasses import dataclass

from flask_login import UserMixin
from sqlalchemy.sql import func
from werkzeug.security import generate_password_hash, check_password_hash

from .shared import db


class User(db.Model, UserMixin):
    __tablename__ = 'user'
    __table_args__ = (db.UniqueConstraint("google_id"), db.UniqueConstraint("username"), db.UniqueConstraint("email"))

    id = db.Column(db.Integer, primary_key=True)

    public_id = db.Column(db.String, default=lambda: str(uuid.uuid4()), nullable=False)

    google_id = db.Column(db.String, nullable=True)
    activated = db.Column(db.Boolean, default=False, server_default="f", nullable=False)

    _password = db.Column(db.String)

    username = db.Column(db.String, nullable=True)
    email = db.Column(db.String, nullable=True)

    last_login = db.Column(db.DateTime, nullable=True)

    notes = db.relationship('Note')

    @property
    def password(self):
        raise AttributeError("Can't read password")

    @password.setter
    def password(self, password):
        self._password = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self._password, password)


@dataclass
class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title: str = db.Column(db.String(50))
    words: int = db.Column(db.Integer)
    progress: int = db.Column(db.Integer)
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    excerpt: str = db.Column(db.String(200))
    content: str = db.Column(db.String(100000))
    user_id: int = db.Column(db.Integer, db.ForeignKey('user.id'))
