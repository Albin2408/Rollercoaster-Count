from app import db
from flask_login import UserMixin

# Model representing a user in the application
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True) 
    username = db.Column(db.String(20), unique=True, nullable=False)  # unique Username 
    email = db.Column(db.String(120), unique=True, nullable=False) 
    password = db.Column(db.String(60), nullable=False)  # User's hashed password 
    # Relationship with the Rollercoaster model, allowing users to own multiple coasters
    coasters = db.relationship('Rollercoaster', backref='author', lazy=True)

# Model representing a roller coaster entry
class Rollercoaster(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # Unique identifier for each roller coaster
    name = db.Column(db.String(100), nullable=False)  # Name of the roller coaster
    location = db.Column(db.String(100), nullable=False)  # Location 
    speed = db.Column(db.String(50), nullable=True)  
    status = db.Column(db.String(50), nullable=True)  
    opening_date = db.Column(db.String(50), nullable=True)  
    manufacturer = db.Column(db.String(100), nullable=True) 
    model = db.Column(db.String(100), nullable=True) 
    height = db.Column(db.String(50), nullable=True)  
    cost = db.Column(db.String(50), nullable=True)  
    ridden = db.Column(db.Boolean, nullable=False, default=False)  
    # Foreign key linking the coaster to the user who added it
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
