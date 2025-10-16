from datetime import datetime, timedelta
from flask import Blueprint, render_template, request, redirect, session, url_for, flash
from app.db import get_db
from app.services import hashing, timeout, db_helper

bp = Blueprint("password", __name__)

#TODO: password requirements, unique users
@bp.route("/register", methods=["GET", "POST"])
def register():
    db = get_db()
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if not hashing.password_strong(password):
            return render_template("register.html", error="Password must contain: <br>- At least 8 characters <br>- Upper and lowercase <br>- At least one number <br>- At least one special character")
        password = hashing.hash_password(password)
        if not db_helper.add_new_user(db, username, password):
            return render_template("register.html", error="Username already taken")

        return redirect("/")

    return render_template("register.html")


@bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":

        username_attempt = request.form["username"]
        password_attempt = request.form["password"]
        db = get_db()
        user = db_helper.get_user_form_username(db, username_attempt)

        if user is None:
            return render_template("login.html", error="Invalid username or password")

        user_id = user["id"]
        password = user["password"]
        failed_attempts = user["failed_attempts"]
        last_lockout = user["last_lockout"]
        lockout_streak = user["lockout_streak"]

        if last_lockout is not None:
            if timeout.is_timeout(last_lockout, lockout_streak):
                remaining = timeout.remaining_minutes(last_lockout, lockout_streak)
                return render_template("login.html", error=f"User {username_attempt} locked out for {remaining} minutes.")

        if hashing.verify_password(password, password_attempt):
            session["user_id"] = user_id
            db_helper.reset_failed_streak(db, user_id)
            return redirect(url_for("main.dashboard"))

        if not timeout.has_remaining_attempts(failed_attempts):
            db_helper.lock_out_user(db, user_id, lockout_streak)
            return render_template("login.html", error=f"User {username_attempt} locked out for {timeout.lockout_duration(lockout_streak)} minutes.")


        db_helper.add_failed_attempt(db, user_id, failed_attempts)
        return render_template("login.html", error="Invalid username or password")

    else:
        return render_template("login.html")