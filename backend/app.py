import os

from flask import Flask, request
from flask_cors import CORS

from dotenv import load_dotenv

# Load environment variables from a local .env file (ignored by git)
BASE_DIR = os.path.dirname(__file__)
load_dotenv(os.path.join(BASE_DIR, ".env"))

from config import SECRET_KEY
from db import init_db
from auth_token import get_bearer_token, verify_token
from routes.auth import auth_bp
from routes.admin import admin_bp
from routes.questions import questions_bp
from routes.timer import timer_bp

app = Flask(__name__)
app.secret_key = SECRET_KEY

# CORS: with credentials, browser requires an explicit origin (no "*").
# Set CORS_ORIGINS to the frontend URL(s), e.g. "http://localhost:5173,https://your-app.vercel.app"
_origins = os.environ.get("CORS_ORIGINS", "http://localhost:5173,http://localhost:3000,http://127.0.0.1:5173,http://127.0.0.1:3000")
_cors_origins = [o.strip() for o in _origins.split(",") if o.strip()]
CORS(app, origins=_cors_origins, supports_credentials=True)

# Session cookie: for cross-origin (frontend on different host), use SameSite=None; Secure (backend must use HTTPS).
app.config["SESSION_COOKIE_SAMESITE"] = os.environ.get("SESSION_COOKIE_SAMESITE", "Lax")
app.config["SESSION_COOKIE_SECURE"] = os.environ.get("SESSION_COOKIE_SECURE", "false").lower() in ("1", "true", "yes")

app.register_blueprint(auth_bp)
app.register_blueprint(admin_bp)
app.register_blueprint(questions_bp)
app.register_blueprint(timer_bp)


@app.before_request
def maybe_fill_session_from_token():
    """If request has valid Bearer token and session is empty, fill session so timer/questions work."""
    from flask import session
    if session.get("username"):
        return
    token = get_bearer_token(request)
    if not token:
        return
    payload = verify_token(token)
    if payload:
        session["user_id"] = payload["user_id"]
        session["username"] = payload["username"]
        session["is_admin"] = payload.get("is_admin", False)


@app.route("/api/health")
def health():
    return {"ok": True}


if __name__ == "__main__":
    init_db()  # creates tables and ensures admin user exists
    app.run(host="0.0.0.0", port=5000, debug=True)
