from app import db
from flask_login import UserMixin

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    coasters = db.relationship('Rollercoaster', backref='author', lazy=True)

class Rollercoaster(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    location = db.Column(db.String(100), nullable=False)
    speed = db.Column(db.String(50), nullable=True)
    status = db.Column(db.String(50), nullable=True)
    opening_date = db.Column(db.String(50), nullable=True)
    manufacturer = db.Column(db.String(100), nullable=True)
    model = db.Column(db.String(100), nullable=True)
    height = db.Column(db.String(50), nullable=True)
    cost = db.Column(db.String(50), nullable=True)
    ridden = db.Column(db.Boolean, nullable=False, default=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
