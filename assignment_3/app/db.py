import sqlite3
from flask import current_app, g

def get_db():
    if "db" not in g:
        g.db = sqlite3.connect(
            current_app.config["DATABASE"],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row
    return g.db

def close_db(e=None):
    db = g.pop("db", None)
    if db is not None:
        db.close()

def init_db(app):
    db_path = app.config["DATABASE"]
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("""
        DROP TABLE IF EXISTS users;
    """)
    conn.commit()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id TEXT PRIMARY KEY NOT NULL,
            username TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL,
            failed_attempts INTEGER DEFAULT 0,
            last_lockout TEXT DEFAULT NULL,
            lockout_streak INTEGER DEFAULT 0,
            totp_secret TEXT,
            two_factor_enabled INTEGER DEFAULT 0
        )
    """)
    conn.commit()
    conn.close()


