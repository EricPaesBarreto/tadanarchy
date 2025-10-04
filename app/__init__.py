from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

db = SQLAlchemy()
login_manager = LoginManager()

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'CHANGE' # change for prod (please)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db' # change for prod (please... again...)

    db.init_app(app)
    login_manager.init_app(app)

    # Import blueprints (and register them)
    from app import routes
    app.register_blueprint(routes.auth)
    app.register_blueprint(routes.main)

    return app