from app import db
from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from .models import User, ParentChild
from flask import Blueprint
from datetime import datetime
import random
from sqlalchemy.exc import SQLAlchemyError


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
        last_name = request.form['last_name']
        email = request.form['email'].lower() # NOT case sensitive (check login query)
        password = request.form['password']
        dob_str = request.form['date_of_birth']

        # should fix issues with date-time inconsistency
        try:
            try:
                dob = datetime.strptime(dob_str, '%Y-%m-%d').date()
            except ValueError:
                try:
                    dob = datetime.strptime(dob_str, '%d/%m/%Y').date()
                except ValueError:
                    flash('Invalid date format')
                    return render_template('authorization/register.html')
        except ValueError:
            flash('Invalid date format')
            return render_template('authorization/register.html') # causes less issues than redirect

        # create new user object
        new_user = User(first_name=first_name, 
                        last_name=last_name, 
                        email=email.lower(), 
                        date_of_birth=dob, 
                        avatar_id=random.randint(0, 4)) # for now, only 4 avatars :(
        new_user.set_password(password)

        # check age --> can they drink alcohol?
        """if not new_user.is_adult():
            db.session.add(new_user)
            db.session.commit()
            flash("Registration successful. Please log in and link with a parent account.")
            return redirect(url_for('auth.login'))"""

        try:
            db.session.add(new_user)
            db.session.commit()
            print("DEBUG: Added user:", new_user.email, new_user.password_hash) # DEBUG DEBUG DEBUG!!!!!!!!
            if not new_user.is_adult(): # check age --> hopefully this version works
                flash("Registration successful. Please log in and link with a parent account.")
                return redirect(url_for('auth.login'))
        except SQLAlchemyError as e:
            db.session.rollback()  # undo partial changes
            flash(f"Registration failed: {str(e)}")
            return render_template('authorization/register.html')

        flash('Registration successful. Please log in.')
        return redirect(url_for('auth.login'))

    return render_template('authorization/register.html')

# LOGIN
@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email'].lower() # NOT case sensitive (check register (sign in logic))
        password = request.form['password']
        user = User.query.filter_by(email=email).first()

        print("DEBUG: login user:", user)
        if user and user.check_password(password):
            print("DEBUG: stored hash:", user.password_hash)
            login_user(user)
            # redirect under-18 to link page
            if not user.is_adult():
                return redirect(url_for('main.link_parent'))
            return redirect(url_for('main.dashboard'))

        flash('Invalid credentials')
        return render_template('authorization/login.html')
    
    return render_template('authorization/login.html') # login for GET (user wasn't in reg prior)
    

# LOGOUT
@auth.route('/logout')
# @login_required                                   # CHANGE FOR PRODDDDDD
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

# UNDER 18 LOGIN 
@main.route('/link_parent', methods=['GET', 'POST'])
# @login_required                                   # CHANGE FOR PRODDDDDD
def link_parent():
    if current_user.is_adult():
        return redirect(url_for('main.dashboard'))

    if request.method == 'POST':
        parent_email = request.form['parent_email']

        # check if this link already exists
        existing = ParentChild.query.filter_by(child_id=current_user.email, parent_id=parent_email).first()
        if existing:
            flash("Link request already sent!")
        else:
            link = ParentChild(child_id=current_user.email, parent_id=parent_email, verified=False)
            db.session.add(link)
            db.session.commit()
            flash(f"DEBUG: verify account for {parent_email}?")  # placeholder for email verification -------------------------> change for production

        return redirect(url_for('main.link_parent'))

    # show all pending links for this child
    links = ParentChild.query.filter_by(child_id=current_user.email).all()
    return render_template('link_parent.html', links=links)


### OTHER FORMS

# CREATE FAMILY (todo)

# DASHBOARD
@main.route('/dashboard')
#@login_required                                   # CHANGE FOR PRODDDDDD
def dashboard():
    return render_template('dashboard.html', user=current_user)
