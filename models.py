from app import db
from flask_login import UserMixin

### ------------------------------
### User Model
### ------------------------------
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    
    # Relationships
    coasters = db.relationship('UserCoaster', backref='user', lazy=True)
    reviews = db.relationship('CoasterReview', backref='reviewer', lazy=True)

### ------------------------------
### Rollercoaster Model
### ------------------------------
class Rollercoaster(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    location = db.Column(db.String(100), nullable=False)
    speed = db.Column(db.String(50), nullable=True)
    status = db.Column(db.String(50), nullable=True)
    manufacturer = db.Column(db.String(100), nullable=True)
    model = db.Column(db.String(100), nullable=True)
    height = db.Column(db.String(50), nullable=True)
    cost = db.Column(db.String(50), nullable=True)
    opening_date = db.Column(db.String(50), nullable=True)
    
    # Relationships
    riders = db.relationship('UserCoaster', backref='coaster', lazy=True)
    reviews = db.relationship('CoasterReview', backref='coaster', lazy=True)

    @property
    def average_rating(self):
        ratings = [review.rating for review in self.reviews if review.rating is not None]
        return round(sum(ratings) / len(ratings), 2) if ratings else None

### ------------------------------
### User-Coaster Relationship Model
### ------------------------------
class UserCoaster(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    coaster_id = db.Column(db.Integer, db.ForeignKey('rollercoaster.id'), nullable=False)
    wishlist = db.Column(db.Boolean, default=False)
    ridden = db.Column(db.Boolean, default=False)
    notes = db.Column(db.Text, nullable=True)  # ✅ Added to store user-specific notes
    rating = db.Column(db.Integer, nullable=True)  # ✅ Added to store user-specific rating

### ------------------------------
### Coaster Reviews Model
### ------------------------------
class CoasterReview(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    coaster_id = db.Column(db.Integer, db.ForeignKey('rollercoaster.id'), nullable=False)
    rating = db.Column(db.Integer, nullable=True)
    review = db.Column(db.Text, nullable=True)

    # Ensure a user can only leave one review per coaster
    __table_args__ = (db.UniqueConstraint('user_id', 'coaster_id', name='unique_review'),)
