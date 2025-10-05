from . import db, login_manager
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import date

# USER
class User(db.Model, UserMixin):
    # properties

    user_id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True, nullable=False)
    first_name = db.Column(db.String(150), nullable=False)
    surname = db.Column(db.String(150), nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    avatar_id = db.Column(db.Integer, default = 0)
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
    
    def has_family(self):
        return self.family_id is not None # family != null
    
    def set_family(self, family):
        if isinstance(family, int): # (family_id passed in)
            self.family_id = family
        else:                       # (family object passed in)
            self.family_id = family.id
    
# FAMILY

class Family(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    parent_email = db.Column(db.String(150))  # The parent which sets up the email
    members = db.relationship('User', backref='family', lazy=True)

# CHILD-PARENT ACCOUNT LINK VERIFICATION 
class ParentChild(db.Model):
    __tablename__ = 'parent_child'

    id = db.Column(db.Integer, primary_key=True)
    parent_id = db.Column(db.String, db.ForeignKey('user.email'), nullable=False)
    child_id = db.Column(db.String, db.ForeignKey('user.email'), nullable=False)
    verified = db.Column(db.Boolean, default=False)  # for future verification feature with emails and stuff

    # relationships (YOU ARE THE FATHER!) *shocked audience*
    parent = db.relationship('User', foreign_keys=[parent_id], backref='children_links')
    child = db.relationship('User', foreign_keys=[child_id], backref='parent_links')


# LOGIN MANAGEMENT

@login_manager.user_loader
def load_user(user_id):
    # get user from database with ID
    return User.query.get(int(user_id))
