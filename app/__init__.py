from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, current_user
from datetime import datetime

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

    from app import models # context (db)

    # create tables --> when changing database for code just clear this for simplicity sake --> (instance/site.db)
    with app.app_context():
        db.create_all()

    @app.context_processor
    def inject_globals(): # so that htmls and jinja don't get confused over user var (store datetime too IG)
        return {
            'user': current_user,
            'current_year': datetime.now().year
        }

    return app
    