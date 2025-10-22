from flask import Blueprint, url_for, session, redirect, current_app
from app.db import get_db
from app.services import hashing, timeout, db_helper

bp = Blueprint("oauth", __name__)


@bp.route('/oauth-login')
def login():
    redirect_uri = url_for('oauth.authorize', _external=True)
    google = current_app.extensions['authlib.integrations.flask_client'].google
    return google.authorize_redirect(redirect_uri)


@bp.route('/authorize')
def authorize():
    google = current_app.extensions['authlib.integrations.flask_client'].google
    token = google.authorize_access_token()
    user = token.get('userinfo')
    if user:
        google_id = user.get('sub')
        email = user.get('email')
        name = user.get('name')


        db = get_db()
        existing_user = db_helper.get_user_form_id(db, google_id)

        if not existing_user:
            # Create new user in database
            db_helper.add_oauth_user(db, google_id, email, "Password1.")

        session['user_id'] = google_id

    return redirect(url_for("main.dashboard"))
