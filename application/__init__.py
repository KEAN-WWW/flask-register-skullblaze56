"""
Main Flask Application Initialization
"""
from flask import Flask
from flask_bootstrap import Bootstrap5
from flask_migrate import Migrate
from flask_wtf import CSRFProtect


from application.database import db
import config
from application.bp.homepage import bp_homepage
from application.bp.authentication import authentication

migrate = Migrate()
csrf = CSRFProtect()


def init_app():
    """Initialize the core application."""
    app = Flask(__name__, instance_relative_config=False)
    app.config.from_object(config.Config())
    csrf.init_app(app)
    bootstrap = Bootstrap5(app)

    # Initialize Plugins
    db.init_app(app)
    migrate.init_app(app, db)

    with app.app_context():

        blueprints = [bp_homepage, authentication]
        # Register Blueprints
        for blueprint in blueprints:
            app.register_blueprint(blueprint)
        return app
