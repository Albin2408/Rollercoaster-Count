from flask import Blueprint, render_template, redirect, url_for, flash, request, abort
from flask_login import login_user, current_user, logout_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash
from app import db
from forms import RegistrationForm, LoginForm, EditCoasterForm, ReviewForm
from models import User, Rollercoaster, UserCoaster, CoasterReview

main = Blueprint('main', __name__)

### ------------------------------
### Home Page (User's Tracked Coasters)
### ------------------------------
@main.route("/")
@login_required
def home():
    filter_type = request.args.get('filter')

    query = UserCoaster.query.filter_by(user_id=current_user.id)

    if filter_type == "ridden":
        coasters = query.filter_by(ridden=True).all()
    elif filter_type == "wishlist":
        coasters = query.filter_by(wishlist=True).all()
    else:
        coasters = query.all()

    return render_template('home.html', coasters=coasters, filter_type=filter_type)

### ------------------------------
### Leaderboard (Top Rated & Most Popular Coasters)
### ------------------------------
@main.route("/leaderboard")
@login_required
def leaderboard():
    coasters = Rollercoaster.query.all()
    sorted_coasters = sorted(coasters, key=lambda c: (c.average_rating or 0, len(c.riders)), reverse=True)

    return render_template('leaderboard.html', coasters=sorted_coasters)

### ------------------------------
### Search for Coasters by Park
### ------------------------------
@main.route("/search_coasters", methods=["GET"])
@login_required
def search_coasters():
    query = request.args.get("query", "").lower()
    coasters = Rollercoaster.query.filter(Rollercoaster.location.ilike(f"%{query}%")).all() if query else []

    return render_template("search_coasters.html", coasters=coasters, query=query)

### ------------------------------
### Track a Coaster (User-Specific)
### ------------------------------
@main.route("/track_coaster/<int:coaster_id>", methods=['POST'])
@login_required
def track_coaster(coaster_id):
    coaster = Rollercoaster.query.get_or_404(coaster_id)

    if UserCoaster.query.filter_by(user_id=current_user.id, coaster_id=coaster_id).first():
        flash("You already have this coaster tracked.", "warning")
        return redirect(url_for("main.home"))

    user_coaster = UserCoaster(user_id=current_user.id, coaster_id=coaster_id)
    db.session.add(user_coaster)
    db.session.commit()
    flash(f'Tracked {coaster.name} successfully!', 'success')

    return redirect(url_for("main.home"))

### ------------------------------
### Edit Tracked Coaster (Personal List)
### ------------------------------
@main.route("/edit_coaster/<int:coaster_id>", methods=['GET', 'POST'])
@login_required
def edit_coaster(coaster_id):
    user_coaster = UserCoaster.query.filter_by(user_id=current_user.id, coaster_id=coaster_id).first_or_404()

    form = EditCoasterForm(obj=user_coaster)

    if form.validate_on_submit():
        user_coaster.wishlist = 'wishlist' in request.form
        user_coaster.ridden = 'ridden' in request.form
        user_coaster.rating = form.rating.data
        user_coaster.notes = form.notes.data

        db.session.commit()
        flash('Coaster updated!', 'success')
        return redirect(url_for('main.home'))

    return render_template('edit_coaster.html', title="Edit Coaster", form=form, coaster=user_coaster)

### ------------------------------
### Submit a Coaster Review
### ------------------------------
@main.route("/review_coaster/<int:coaster_id>", methods=['GET', 'POST'])
@login_required
def review_coaster(coaster_id):
    coaster = Rollercoaster.query.get_or_404(coaster_id)
    review = CoasterReview.query.filter_by(user_id=current_user.id, coaster_id=coaster_id).first()

    form = ReviewForm(obj=review)

    if form.validate_on_submit():
        if review:
            review.rating = form.rating.data
            review.review = form.review.data
        else:
            new_review = CoasterReview(user_id=current_user.id, coaster_id=coaster_id,
                                       rating=form.rating.data, review=form.review.data)
            db.session.add(new_review)

        db.session.commit()
        flash("Review submitted successfully!", "success")
        return redirect(url_for("main.home"))

    return render_template("review_coaster.html", title="Review Coaster", form=form, coaster=coaster)

### ------------------------------
### Delete Tracked Coaster
### ------------------------------
@main.route("/delete_coaster/<int:coaster_id>", methods=["POST"])
@login_required
def delete_coaster(coaster_id):
    user_coaster = UserCoaster.query.filter_by(user_id=current_user.id, coaster_id=coaster_id).first_or_404()

    db.session.delete(user_coaster)
    db.session.commit()
    flash('Coaster removed from your list.', 'success')
    return redirect(url_for('main.home'))

### ------------------------------
### User Authentication (Register/Login/Logout)
### ------------------------------
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
            return redirect(url_for('main.home'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')

    return render_template('login.html', title='Login', form=form)

@main.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('main.login'))
