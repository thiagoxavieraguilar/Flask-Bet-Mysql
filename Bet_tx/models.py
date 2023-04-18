from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    username = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    date_created = db.Column(db.DateTime(timezone=True), default=func.now())
    bets = db.relationship('Bet', backref='user', passive_deletes=True)
    


class Bet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    matches_bet = db.Column(db.Text, nullable=False)
    odd_final = db.Column(db.Float(), nullable=False)
    value_bet = db.Column(db.Float(),nullable=False)
    return_bet=db.Column(db.Float(), nullable=False)
    date_created = db.Column(db.DateTime(timezone=True), default=func.now())
    author = db.Column(db.Integer, db.ForeignKey('user.id', ondelete="CASCADE"), nullable=False)
    