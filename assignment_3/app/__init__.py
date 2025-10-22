import os
from datetime import timedelta
from authlib.integrations.flask_client import OAuth
from dotenv import load_dotenv

from flask import Flask
from app.db import init_db, close_db

load_dotenv()

def create_app():
    oauth = OAuth()
    app = Flask(__name__)
    app.config["DATABASE"] = os.path.join(app.instance_path, "database.db")

    app.config["SECRET_KEY"] = os.urandom(24) # Ensures cookies cant be tampered with
    app.config["SESSION_COOKIE_SECURE"] = True # HTTP localhost allowed
    app.config["SESSION_COOKIE_HTTPONLY"] = True # HttpOnly
    app.config["PERMANENT_SESSION_LIFETIME"] = timedelta(minutes=30) # Lifetime

    # Ensure instance folder exists
    os.makedirs(app.instance_path, exist_ok=True)

    # Initialize the database
    init_db(app)

    # Initialize OAuth with app
    oauth.init_app(app)

    # Configure OAuth with Google
    oauth.register(
        name='google',
        client_id=os.getenv('GOOGLE_CLIENT_ID'),
        client_secret=os.getenv("GOOGLE_CLIENT_SECRET"),
        server_metadata_url='https://accounts.google.com/.well-known/openid-configuration',
        client_kwargs={'scope': 'openid email profile'}
    )

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
