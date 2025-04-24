"""
Application Factory Module
"""
from flask import Flask
from flask_bootstrap import Bootstrap5
from flask_migrate import Migrate
from flask_wtf import CSRFProtect
from flask_login import LoginManager

from application.database import db
from application.config import Config
from application.bp.homepage import bp_homepage
from application.bp.authentication import authentication

migrate = Migrate()
csrf = CSRFProtect()
login_manager = LoginManager()

@login_manager.user_loader
def load_user(user_id):
    from application.models import User
    return User.query.get(int(user_id))

def create_app(config_name='default'):
    """Initialize the core application."""
    app = Flask(__name__, instance_relative_config=False)
    
    if config_name == 'testing':
        app.config.update({
            'TESTING': True,
            'WTF_CSRF_ENABLED': False,
            'SQLALCHEMY_DATABASE_URI': 'sqlite:///:memory:',
            'SQLALCHEMY_TRACK_MODIFICATIONS': False,
            'SECRET_KEY': 'test-secret-key'
        })
    else:
        app.config.from_object(Config)
    
    csrf.init_app(app)
    Bootstrap5(app)
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)

    with app.app_context():
        db.create_all()
        app.register_blueprint(bp_homepage)
        app.register_blueprint(authentication)
    
    return app 