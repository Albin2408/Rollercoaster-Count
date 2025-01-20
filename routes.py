from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify, abort
from flask_login import login_user, current_user, logout_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash
from app import db
from forms import RegistrationForm, LoginForm, AddCoasterForm, WeatherForm
from models import User, Rollercoaster
import requests

main = Blueprint('main', __name__)

@main.route("/")
@login_required
def home():
    park = request.args.get('park')
    if park:
        coasters = Rollercoaster.query.filter_by(user_id=current_user.id, location=park).all()
    else:
        coasters = Rollercoaster.query.filter_by(user_id=current_user.id).all()
    return render_template('home.html', coasters=coasters)

@main.route("/coaster_count")
@login_required
def coaster_count():
    park = request.args.get('park')
    if park:
        coasters = Rollercoaster.query.filter_by(user_id=current_user.id, location=park).all()
    else:
        coasters = Rollercoaster.query.filter_by(user_id=current_user.id).all()
    return render_template('coaster_count.html', coasters=coasters)

@main.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data)
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('main.login'))
    return render_template('register.html', title='Register', form=form)

@main.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page or url_for('main.home'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)

@main.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('main.login'))

@main.route("/add_coaster", methods=['GET', 'POST'])
@login_required
def add_coaster():
    form = AddCoasterForm()
    if form.validate_on_submit():
        coaster = Rollercoaster(name=form.coaster.data, location=form.park.data, author=current_user)
        db.session.add(coaster)
        db.session.commit()
        flash('Coaster added!', 'success')
        return redirect(url_for('main.coaster_count'))
    return render_template('add_coaster.html', title='Add Coaster', form=form)

@main.route("/mark_ridden/<int:coaster_id>")
@login_required
def mark_ridden(coaster_id):
    coaster = Rollercoaster.query.get_or_404(coaster_id)
    if coaster.author != current_user:
        abort(403)
    coaster.ridden = True
    db.session.commit()
    flash('Coaster marked as ridden!', 'success')
    return redirect(url_for('main.coaster_count'))

@main.route("/search_coasters")
@login_required
def search_coasters():
    query = request.args.get('query', '').lower()
    parks = Rollercoaster.query.with_entities(Rollercoaster.location.distinct()).filter(Rollercoaster.location.ilike(f"%{query}%")).all()
    return jsonify([park[0] for park in parks])

@main.route("/weather", methods=['GET', 'POST'])
@login_required
def weather():
    form = WeatherForm()
    weather_data = None

    if form.validate_on_submit() or request.method == 'GET':
        zipcode = form.zipcode.data or request.args.get('zipcode')
        if zipcode:
            api_key = '860de6d5fcb1751652a81e929550c60a'
            url = f'http://api.openweathermap.org/data/2.5/forecast?zip={zipcode},us&appid={api_key}&units=imperial'
            response = requests.get(url)
            if response.status_code == 200:
                weather_data = response.json()['list']
            else:
                flash('Invalid zipcode or no weather data available.', 'danger')

    return render_template('weather.html', title='Weather', form=form, weather_data=weather_data)
