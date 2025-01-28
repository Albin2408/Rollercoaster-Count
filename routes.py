from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify, abort
from flask_login import login_user, current_user, logout_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash
from app import db
from forms import RegistrationForm, LoginForm, AddCoasterForm, WeatherForm
from models import User, Rollercoaster
import requests


main = Blueprint('main', __name__)

# Home route that displays coasters for the logged-in user
@main.route("/")
@login_required
def home():
    park = request.args.get('park')  # Filter coasters by park if specified
    if park:
        coasters = Rollercoaster.query.filter_by(user_id=current_user.id, location=park).all()
    else:
        coasters = Rollercoaster.query.filter_by(user_id=current_user.id).all()
    return render_template('home.html', coasters=coasters)

# Route to display coaster count for the logged-in user
@main.route("/coaster_count")
@login_required
def coaster_count():
    park = request.args.get('park')  # Filter coasters by park if specified
    if park:
        coasters = Rollercoaster.query.filter_by(user_id=current_user.id, location=park).all()
    else:
        coasters = Rollercoaster.query.filter_by(user_id=current_user.id).all()
    return render_template('coaster_count.html', coasters=coasters)

# Route for user registration
@main.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:  # Redirect logged-in users to the home page
        return redirect(url_for('main.home'))
    form = RegistrationForm()
    if form.validate_on_submit():  # Handle form submission and create a new user
        hashed_password = generate_password_hash(form.password.data)
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('main.login'))
    return render_template('register.html', title='Register', form=form)

# Route for user login
@main.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:  # Redirect logged-in users to the home page
        return redirect(url_for('main.home'))
    form = LoginForm()
    if form.validate_on_submit():  # Handle form submission and authenticate user
        user = User.query.filter_by(email=form.email.data).first()
        if user and check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')  # Redirect to the next page if specified
            return redirect(next_page or url_for('main.home'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)

# Route for user logout
@main.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('main.login'))

# Route to add a new roller coaster
@main.route("/add_coaster", methods=['GET', 'POST'])
@login_required
def add_coaster():
    form = AddCoasterForm()
    if form.validate_on_submit():  # Add coaster to the database
        coaster = Rollercoaster(name=form.coaster.data, location=form.park.data, author=current_user)
        db.session.add(coaster)
        db.session.commit()
        flash('Coaster added!', 'success')
        return redirect(url_for('main.coaster_count'))
    return render_template('add_coaster.html', title='Add Coaster', form=form)

# Route to mark a roller coaster as ridden
@main.route("/mark_ridden/<int:coaster_id>")
@login_required
def mark_ridden(coaster_id):
    coaster = Rollercoaster.query.get_or_404(coaster_id)  # Get coaster or return 404
    if coaster.author != current_user:  # Ensure the current user owns the coaster
        abort(403)
    coaster.ridden = True
    db.session.commit()
    flash('Coaster marked as ridden!', 'success')
    return redirect(url_for('main.coaster_count'))

# Route to search for coasters by park
@main.route("/search_coasters")
@login_required
def search_coasters():
    query = request.args.get('query', '').lower()
    # Fetch distinct parks matching the query
    parks = Rollercoaster.query.with_entities(Rollercoaster.location.distinct()).filter(Rollercoaster.location.ilike(f"%{query}%")).all()
    return jsonify([park[0] for park in parks])

# Route to display weather forecast for a specified park
@main.route("/weather", methods=['GET', 'POST'])
@login_required
def weather():
    form = WeatherForm()
    weather_data = None

    if form.validate_on_submit() or request.method == 'GET':  # Handle form submission or GET request
        zipcode = form.zipcode.data or request.args.get('zipcode')  # Get ZIP code from form or query
        if zipcode:
            api_key = ''  # Add your OpenWeatherMap API key here
            url = f'http://api.openweathermap.org/data/2.5/forecast?zip={zipcode},us&appid={api_key}&units=imperial'
            response = requests.get(url)
            if response.status_code == 200:  # Parse weather data if request is successful
                weather_data = response.json()['list']
            else:
                flash('Invalid zipcode or no weather data available.', 'danger')

    return render_template('weather.html', title='Weather', form=form, weather_data=weather_data)
