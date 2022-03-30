import os

from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
from werkzeug.exceptions import HTTPException
from app.logger import log

# instantiate extensions
login_manager = LoginManager()
db = SQLAlchemy()



def create_app(environment="development"):

    from config import config
    from app.views import (
        main_blueprint,
        auth_blueprint,
    )
    from app.models import (
        User,
    )

    # Instantiate app.
    app = Flask(__name__)
    
    # Migrations setup
    migrate = Migrate(app, db)

    # Set app config.
    env = os.environ.get("FLASK_ENV", environment)
    log(log.INFO, "App environment: %s", env)
    app.config.from_object(config[env])
    config[env].configure(app)

    # Set up extensions.
    db.init_app(app)
    login_manager.init_app(app)

    # Register blueprints.
    app.register_blueprint(auth_blueprint)
    app.register_blueprint(main_blueprint)

    # Set up flask login.
    @login_manager.user_loader
    def get_user(id):
        return User.query.get(int(id))

    login_manager.login_view = "auth.login"
    login_manager.login_message_category = "info"

    # Error handlers.
    @app.errorhandler(HTTPException)
    def handle_http_error(exc):
        log(log.ERROR, "Error code %d", exc.code)
        return render_template("error.html", error=exc), exc.code

    return app
