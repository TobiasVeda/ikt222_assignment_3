from datetime import datetime

def get_user_form_username(db, username):
    return db.execute("SELECT * FROM users WHERE username = ?", (username,)).fetchone()

def get_user_form_id(db, user_id):
    return db.execute("SELECT * FROM users WHERE id = ?", (user_id,)).fetchone()

def add_new_user(db, username, password):
    db.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
    db.commit()

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

