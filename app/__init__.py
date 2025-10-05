from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, current_user
from datetime import datetime

db = SQLAlchemy()
login_manager = LoginManager()


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'CHANGE'  # Change for production
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # init
    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'  # automatic redirect for @login_required

    # blueprints
    from app import routes
    app.register_blueprint(routes.auth)
    app.register_blueprint(routes.main)

    # models, tables IMPORTANT FOR DB
    from app import models
    with app.app_context():
        db.create_all()

    # so jinja doesn't get confused with vars
    @app.context_processor
    def inject_globals():
        return {
            'user': current_user,
            'current_year': datetime.now().year
        }

    return app
