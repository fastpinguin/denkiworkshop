from . import db 
from flask_login import UserMixin


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True) # primary keys are required by SQLAlchemy
    username = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))

    def __str__(self) -> str:
        return self.username


class Player(db.Model):
    playerid = db.Column(db.String(100), unique=True, primary_key=True)
    points = db.Column(db.Text)