from app import db
from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from .models import User
from flask import Blueprint
from datetime import datetime
import random

 # blueprints (everything exists here anyways, but just in case *shrug*)
auth = Blueprint('auth', __name__)
main = Blueprint('main', __name__)

### PAGES

# MAIN
@main.route('/')
def home():
    return render_template('landing_page.html')


### ACCOUNTS

# SIGN-IN
@auth.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        first_name = request.form['first_name']
        surname = request.form['surname']
        email = request.form['email']
        password = request.form['password']
        dob_str = request.form['date_of_birth']

        try:
            dob = datetime.strptime(dob_str, '%d-%m-%Y').date()
        except ValueError:
            flash('Invalid date format')
            return redirect(url_for('auth.register'))

        # create new user object
        new_user = User(first_name=first_name, surname=surname, email=email, date_of_birth=dob, avatar_id=random.randint(1, 5)) #
        new_user.set_password(password)

        # check age --> can they drink alcohol?
        """if not new_user.is_adult():
            flash('You must be assigned to a parent's email')
            return redirect(url_for('auth.register'))"""

        db.session.add(new_user)
        db.session.commit()

        flash('Registration successful. Please log in.')
        return redirect(url_for('auth.login'))

    return render_template('landing_page.html')

# LOGIN
@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()

        if user and user.check_password(password):
            login_user(user)
            return redirect(url_for('main.dashboard'))
        flash('Invalid credentials')
    return render_template('landing_page.html')

# LOGOUT
@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

### OTHER FORMS

# CREATE FAMILY (todo)

# DASHBOARD
@main.route('/dashboard')
@login_required
def dashboard():
    return render_template('main_page.html', user=current_user)
