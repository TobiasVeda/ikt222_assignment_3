import os
from datetime import timedelta

from flask import Flask
from app.db import init_db, close_db

def create_app():
    app = Flask(__name__)
    app.config['DATABASE'] = os.path.join(app.instance_path, 'database.db')

    app.config['SECRET_KEY'] = os.urandom(24) # Ensures cookies cant be tampered with
    app.config['SESSION_COOKIE_SECURE'] = False # false when dev on http
    app.config['SESSION_COOKIE_HTTPONLY'] = True
    app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=30)

    # Ensure instance folder exists
    os.makedirs(app.instance_path, exist_ok=True)

    # Initialize the database
    init_db(app)

    # Register blueprints
    from .routes.main import bp as main_bp
    from .routes.password_auth import bp as password_bp
    from .routes.two_factor import bp as two_factor_bp
    from .routes.oauth import bp as oauth_bp
    app.register_blueprint(main_bp)
    app.register_blueprint(password_bp)
    app.register_blueprint(two_factor_bp)
    app.register_blueprint(oauth_bp)

    # Register teardown to close DB after each request
    @app.teardown_appcontext
    def teardown_db(exception):
        close_db()

    return app
