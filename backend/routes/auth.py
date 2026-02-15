from flask import Blueprint, request, jsonify, session

from db import check_login

auth_bp = Blueprint("auth", __name__, url_prefix="/api/auth")

# Login uses POST body only (no password in URL). Use HTTPS in production.


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

    is_admin = username == "admin"
    session["username"] = user["username"]
    session["user_id"] = user["id"]
    session["is_admin"] = is_admin
    return jsonify({
        "ok": True,
        "is_admin": is_admin,
        "username": user["username"],
    })


@auth_bp.route("/logout", methods=["POST"])
def logout():
    session.clear()
    return jsonify({"ok": True})


@auth_bp.route("/me", methods=["GET"])
def me():
    if not session.get("username"):
        return jsonify({"ok": False, "user": None}), 401
    return jsonify({
        "ok": True,
        "user": {
            "username": session["username"],
            "is_admin": session.get("is_admin", False),
        },
    })
