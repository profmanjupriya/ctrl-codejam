import sqlite3
import os
from typing import Tuple

from werkzeug.security import generate_password_hash, check_password_hash

from config import DATABASE

# Admin is stored in DB with hashed password; this is only for ensuring admin exists on init
ADMIN_USERNAME = "admin"
ADMIN_DEFAULT_PASSWORD = "code"


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
    """Ensure admin user exists with hashed password. Migrate plaintext admin password to hash if needed."""
    conn = get_db()
    row = conn.execute("SELECT id, password FROM users WHERE username = ?", (ADMIN_USERNAME,)).fetchone()
    hashed = generate_password_hash(ADMIN_DEFAULT_PASSWORD)
    if not row:
        conn.execute(
            "INSERT INTO users (username, password) VALUES (?, ?)",
            (ADMIN_USERNAME, hashed),
        )
    elif not _is_hashed(row["password"]):
        conn.execute("UPDATE users SET password = ? WHERE username = ?", (hashed, ADMIN_USERNAME))
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
