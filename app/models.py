from . import db, login_manager
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import date

# user
class User(db.Model, UserMixin):
    # properties

    email = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(150), unique=True, nullable=False)
    surname = db.Column(db.String(150), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    avatar_id = db.Column(db.Integer, default = 1)
    points = db.Column(db.Integer, default = 0)
    date_of_birth = db.Column(db.Date, nullable = False)
    family_id = db.Column(db.Integer, db.ForeignKey('family.id'), nullable=True)

    # methods

    def set_password(self, password):
        # store password HASH in the database
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        # checks the inputed password against HASH in the database
        return check_password_hash(self.password_hash, password)
    
    def is_adult(self):
        today = date.today()
        dob = self.date_of_birth
        age = today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))
        return age >= 18
    
    def is_child(self):
        return not self.is_adult() # just reverse it LMAO
    
### family

class Family(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    parent_email = db.Column(db.String(150))  # The parent which sets up the email
    members = db.relationship('User', backref='family', lazy=True)

## login management

@login_manager.user_loader
def load_user(user_id):
    # get user from database with ID
    return User.query.get(int(user_id))
