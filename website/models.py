from dataclasses import dataclass
from sqlalchemy.sql import func
from .shared import db
from flask_login import UserMixin


@dataclass
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username: str = db.Column(db.String(150), unique=True)
    email: str = db.Column(db.String(150), unique=True)
    password: str = db.Column(db.String(150))
    notes = db.relationship('Note')


@dataclass
class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title: str = db.Column(db.String(50))
    words = db.Column(db.Integer)
    progress = db.Column(db.Integer)
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    excerpt = db.Column(db.String(200))
    content = db.Column(db.String(100000))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
