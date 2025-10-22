
from flask import Blueprint, render_template, redirect, session, url_for
from app.db import get_db
from app.services import db_helper

bp = Blueprint("main", __name__)

# Home page
@bp.route("/", methods=("GET", "POST"))
def index():
    return render_template("index.html")

# Dashboard. Require login
@bp.route("/dashboard", methods=("GET", "POST"))
def dashboard():
    # is cookie "user_id" present
    if "user_id" in session:
        db = get_db()
        user = db_helper.get_user_form_id(db, session["user_id"])
        two_factor_enabled = db_helper.is_2fa_enabled(db, session["user_id"])
        return render_template("dashboard.html",
                             user=user["username"],
                             two_factor_enabled=two_factor_enabled)

    return redirect(url_for("main.index"))