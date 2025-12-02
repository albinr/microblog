"""
Factory for application
"""

import os
import logging
import sentry_sdk
from logging.handlers import RotatingFileHandler
from flask import Flask
from flask.logging import default_handler
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_moment import Moment
from flask_bootstrap import Bootstrap
from app.config import ProdConfig, RequestFormatter
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__) +  "/..")
load_dotenv(os.path.join(basedir, '.env'))

db = SQLAlchemy()
migrate = Migrate()
login = LoginManager()
login.login_view = 'auth.login'
login.login_message = 'Please log in to access this page.'
bootstrap = Bootstrap()
moment = Moment()



def create_app(config_class=ProdConfig):
    """
    Create flask app, init addons, blueprints and setup logging
    """

    if os.environ.get("SENTRY_DSN"):
        sentry_sdk.init(
            dsn=os.environ.get("SENTRY_DSN"),
            # Add data like request headers and IP for users,
            # see https://docs.sentry.io/platforms/python/data-management/data-collected/ for more info
            send_default_pii=True,
            # Enable sending logs to Sentry
            enable_logs=True,
            # Set traces_sample_rate to 1.0 to capture 100%
            # of transactions for tracing.
            traces_sample_rate=1.0,
            # Set profile_session_sample_rate to 1.0 to profile 100%
            # of profile sessions.
            profile_session_sample_rate=1.0,
            # Set profile_lifecycle to "trace" to automatically
            # run the profiler on when there is an active transaction
            profile_lifecycle="trace",
        )
        logging.info("Sentry initialized")
        print("Sentry initialized")
    else:
        logging.warning("SENTRY_DSN not found, Sentry not initialized")
        print("SENTRY_DSN not found, Sentry not initialized")

    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    migrate.init_app(app, db)
    login.init_app(app)
    moment.init_app(app)
    bootstrap.init_app(app)
    

    #pylint: disable=wrong-import-position, cyclic-import, import-outside-toplevel
    from app.errors import bp as errors_bp
    app.register_blueprint(errors_bp)

    from app.auth import bp as auth_bp
    app.register_blueprint(auth_bp)

    from app.main import bp as main_bp
    app.register_blueprint(main_bp)
    #pylint: enable=wrong-import-position, cyclic-import, import-outside-toplevel


    if not app.debug and not app.testing:
        formatter = RequestFormatter(
            '[%(asctime)s %(levelname)s] %(remote_addr)s requested %(url)s\n: %(message)s [in %(module)s:%(lineno)d]'
        )
        default_handler.setFormatter(formatter)
        app.logger.setLevel(logging.INFO)

    return app


from app import models #pylint: disable=wrong-import-position, cyclic-import, import-outside-toplevel
