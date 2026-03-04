import sqlite3
import os
import time
from typing import Tuple

from werkzeug.security import generate_password_hash, check_password_hash

from config import DATABASE

# Admin is stored in DB with hashed password; this is only for ensuring admin exists on init.
# The initial admin username and password are provided via environment variables so they are
# not hard-coded in the repository.
ADMIN_USERNAME = os.environ.get("ADMIN_USERNAME", "admin")
ADMIN_DEFAULT_PASSWORD = os.environ.get("ADMIN_DEFAULT_PASSWORD", "code")


def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_db()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    """)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS scores (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            score INTEGER NOT NULL,
            completed_at REAL,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    """)
    conn.commit()
    conn.close()
    ensure_admin()


def _is_hashed(password_value: str) -> bool:
    """Werkzeug hashes start with 'scrypt:' or 'pbkdf2:'."""
    return password_value.startswith("scrypt:") or password_value.startswith("pbkdf2:")


def ensure_admin():
    """Ensure admin user exists with hashed password based on env vars."""
    conn = get_db()
    row = conn.execute(
        "SELECT id, password FROM users WHERE username = ?",
        (ADMIN_USERNAME,),
    ).fetchone()
    hashed = generate_password_hash(ADMIN_DEFAULT_PASSWORD)
    if not row:
        # Create admin with env-provided credentials
        conn.execute(
            "INSERT INTO users (username, password) VALUES (?, ?)",
            (ADMIN_USERNAME, hashed),
        )
    else:
        # Always sync admin password to the current env value
        conn.execute(
            "UPDATE users SET password = ? WHERE username = ?",
            (hashed, ADMIN_USERNAME),
        )
    conn.commit()
    conn.close()


def create_user(username: str, password: str) -> Tuple[bool, str]:
    """Create user with hashed password. Returns (success, error_message)."""
    username = username.strip()
    if not username or not password:
        return False, "Username and password required"
    try:
        conn = get_db()
        conn.execute(
            "INSERT INTO users (username, password) VALUES (?, ?)",
            (username, generate_password_hash(password)),
        )
        conn.commit()
        conn.close()
        return True, ""
    except sqlite3.IntegrityError:
        return False, "Username already exists"


def check_login(username: str, password: str) -> dict | None:
    conn = get_db()
    row = conn.execute("SELECT id, username, password FROM users WHERE username = ?", (username.strip(),)).fetchone()
    conn.close()
    if not row or not check_password_hash(row["password"], password):
        return None
    return {"id": row["id"], "username": row["username"]}


def get_all_users():
    """Return list of {id, username} (no passwords)."""
    conn = get_db()
    rows = conn.execute(
        "SELECT id, username FROM users ORDER BY username COLLATE NOCASE"
    ).fetchall()
    conn.close()
    return [{"id": r["id"], "username": r["username"]} for r in rows]


def delete_user(user_id: int) -> Tuple[bool, str]:
    """Delete user by id. Cannot delete admin. Returns (success, error_message)."""
    conn = get_db()
    row = conn.execute("SELECT username FROM users WHERE id = ?", (user_id,)).fetchone()
    if not row:
        conn.close()
        return False, "User not found"
    if row["username"] == ADMIN_USERNAME:
        conn.close()
        return False, "Cannot delete admin"
    conn.execute("DELETE FROM users WHERE id = ?", (user_id,))
    conn.commit()
    conn.close()
    return True, ""


def update_user_password(user_id: int, new_password: str) -> Tuple[bool, str]:
    """Update user password by id. Returns (success, error_message)."""
    if not new_password:
        return False, "Password required"
    conn = get_db()
    cur = conn.execute("UPDATE users SET password = ? WHERE id = ?", (generate_password_hash(new_password), user_id))
    conn.commit()
    conn.close()
    if cur.rowcount == 0:
        return False, "User not found"
    return True, ""


def clear_users_except_admin():
    """Remove all users except admin. Returns number deleted."""
    conn = get_db()
    cur = conn.execute("DELETE FROM users WHERE username != ?", (ADMIN_USERNAME,))
    n = cur.rowcount
    conn.commit()
    conn.close()
    return n


def record_score(user_id: int, points: int):
    """Record points awarded to a user (for leaderboard)."""
    if points <= 0:
        return
    conn = get_db()
    conn.execute(
        "INSERT INTO scores (user_id, score, completed_at) VALUES (?, ?, ?)",
        (user_id, points, time.time()),
    )
    conn.commit()
    conn.close()


def get_leaderboard():
    """Return list of { username, score } for all non-admin users, sorted by score descending."""
    conn = get_db()
    rows = conn.execute("""
        SELECT u.username, COALESCE(SUM(s.score), 0) AS total
        FROM users u
        LEFT JOIN scores s ON u.id = s.user_id
        WHERE u.username != ?
        GROUP BY u.id
        ORDER BY total DESC, u.username
    """, (ADMIN_USERNAME,)).fetchall()
    conn.close()
    return [{"username": r["username"], "score": int(r["total"])} for r in rows]
