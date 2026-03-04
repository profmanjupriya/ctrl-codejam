from flask import Blueprint, request, jsonify, session

from db import check_login, ADMIN_USERNAME
from auth_token import make_token, get_bearer_token, verify_token

auth_bp = Blueprint("auth", __name__, url_prefix="/api/auth")

# Login uses POST body only (no password in URL). Use HTTPS in production.
# Returns a bearer token so the frontend can send it in Authorization header when the session cookie is not sent (e.g. cross-origin).


@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json() or {}
    username = (data.get("username") or "").strip()
    password = data.get("password") or ""

    if not username or not password:
        return jsonify({"ok": False, "error": "Username and password required"}), 400

    user = check_login(username, password)
    if not user:
        return jsonify({"ok": False, "error": "Invalid login"}), 401

    is_admin = username == ADMIN_USERNAME
    session["username"] = user["username"]
    session["user_id"] = user["id"]
    session["is_admin"] = is_admin
    token = make_token(user["id"], user["username"], is_admin)
    return jsonify({
        "ok": True,
        "is_admin": is_admin,
        "username": user["username"],
        "token": token,
    })


@auth_bp.route("/logout", methods=["POST"])
def logout():
    session.clear()
    return jsonify({"ok": True})


@auth_bp.route("/me", methods=["GET"])
def me():
    # Prefer bearer token so it works cross-origin when cookie is not sent
    token = get_bearer_token(request)
    if token:
        payload = verify_token(token)
        if payload:
            return jsonify({
                "ok": True,
                "user": {
                    "username": payload["username"],
                    "is_admin": payload.get("is_admin", False),
                },
            })
    if session.get("username"):
        return jsonify({
            "ok": True,
            "user": {
                "username": session["username"],
                "is_admin": session.get("is_admin", False),
            },
        })
    return jsonify({"ok": False, "user": None}), 401
