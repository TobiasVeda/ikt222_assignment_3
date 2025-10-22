import uuid
from datetime import datetime


# Hides SQL from rest of code by putting in functions here

def get_user_form_username(db, username):
    return db.execute("SELECT * FROM users WHERE username = ?", (username,)).fetchone()


def get_user_form_id(db, user_id):
    return db.execute("SELECT * FROM users WHERE id = ?", (user_id,)).fetchone()


def add_new_user(db, username, password):
    test = db.execute("SELECT 1 FROM users WHERE username = ? LIMIT 1", (username,))
    if test.fetchone() is None:
        user_id = str(uuid.uuid4())
        db.execute("INSERT INTO users (id, username, password) VALUES (?, ?, ?)", (user_id, username, password))
        db.commit()
        return True

    return False


def add_oauth_user(db, user_id, username, password):
    test = db.execute("SELECT * FROM users WHERE id = ?", (user_id,)).fetchone()
    if test is None:
        db.execute(
            'INSERT INTO users (id, username, password) VALUES (?, ?, ?)',
            (user_id, username, password)
        )
        db.commit()
        return True

    return False


def reset_failed_streak(db, user_id):
    db.execute("UPDATE users SET failed_attempts = ?, lockout_streak = ? WHERE id = ?", (0, 0, user_id,))
    db.commit()


def lock_out_user(db, user_id, lockout_streak):
    db.execute("UPDATE users SET failed_attempts = 0, last_lockout = ?, lockout_streak = ? WHERE id = ?",
               (datetime.now(), lockout_streak + 1, user_id,))
    db.commit()


def add_failed_attempt(db, user_id, failed_attempts):
    db.execute("UPDATE users SET failed_attempts = ? WHERE id = ?", (failed_attempts + 1, user_id,))
    db.commit()


def enable_2fa_for_user(db, user_id, totp_secret):
    db.execute(
        "UPDATE users SET totp_secret = ?, two_factor_enabled = 1 WHERE id = ?",
        (totp_secret, user_id)
    )
    db.commit()
    return True

def disable_2fa_for_user(db, user_id):
    db.execute(
        "UPDATE users SET totp_secret = NULL, two_factor_enabled = 0 WHERE id = ?",
        (user_id,)
    )
    db.commit()
    return True


def is_2fa_enabled(db, user_id):
    user = db.execute(
        "SELECT two_factor_enabled, totp_secret FROM users WHERE id = ?",
        (user_id,)
    ).fetchone()

    if user:
        return user["two_factor_enabled"] == 1 and user["totp_secret"] is not None
    return False