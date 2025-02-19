from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, BooleanField, IntegerField, TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo, NumberRange, Optional

### ------------------------------
### User Authentication Forms
### ------------------------------
class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')

### ------------------------------
### Coaster Tracking Form
### ------------------------------
class EditCoasterForm(FlaskForm):
    wishlist = BooleanField('Wishlist (Want to ride)', default=False)
    ridden = BooleanField('Ridden', default=False)  
    rating = IntegerField('Your Rating (1-10)', validators=[Optional(), NumberRange(min=1, max=10)]) 
    notes = TextAreaField('Personal Notes', validators=[Optional()])  
    submit = SubmitField('Save Changes')

### ------------------------------
### Coaster Review Form
### ------------------------------
class ReviewForm(FlaskForm):
    rating = IntegerField('Rating (1-10)', validators=[DataRequired(), NumberRange(min=1, max=10)])
    review = TextAreaField('Write a review...', validators=[Optional()])
    submit = SubmitField('Submit Review')

### ------------------------------
### Weather Lookup Form
### ------------------------------
class WeatherForm(FlaskForm):
    zipcode = StringField('Zipcode', validators=[DataRequired(), Length(min=5, max=5)])
    submit = SubmitField('Get Weather')
