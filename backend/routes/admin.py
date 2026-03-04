from flask import Blueprint, request, jsonify, session

from db import get_all_users, create_user, delete_user, update_user_password, clear_users_except_admin, get_leaderboard
from timer_service import start_exam, pause_exam, get_status

admin_bp = Blueprint("admin", __name__, url_prefix="/api/admin")


def require_admin():
    if not session.get("is_admin"):
        return False
    return True


@admin_bp.route("/start-exam", methods=["POST"])
def start_exam_route():
    if not require_admin():
        return jsonify({"ok": False, "error": "Admin only"}), 403
    start_exam()
    return jsonify({"ok": True, "message": "Exam timer started"})


@admin_bp.route("/pause-exam", methods=["POST"])
def pause_exam_route():
    if not require_admin():
        return jsonify({"ok": False, "error": "Admin only"}), 403
    pause_exam()
    return jsonify({"ok": True, "message": "Exam timer paused"})


@admin_bp.route("/timer-status", methods=["GET"])
def timer_status():
    if not require_admin():
        return jsonify({"ok": False, "error": "Admin only"}), 403
    return jsonify({"ok": True, **get_status()})


@admin_bp.route("/leaderboard", methods=["GET"])
def leaderboard():
    if not require_admin():
        return jsonify({"ok": False, "error": "Admin only"}), 403
    entries = get_leaderboard()
    return jsonify({"ok": True, "leaderboard": entries})


@admin_bp.route("/users", methods=["GET"])
def list_users():
    if not require_admin():
        return jsonify({"ok": False, "error": "Admin only"}), 403
    users = get_all_users()
    return jsonify({"ok": True, "users": users})


@admin_bp.route("/users", methods=["POST"])
def add_user():
    if not require_admin():
        return jsonify({"ok": False, "error": "Admin only"}), 403
    data = request.get_json() or {}
    username = (data.get("username") or "").strip()
    password = data.get("password") or ""
    ok, err = create_user(username, password)
    if not ok:
        return jsonify({"ok": False, "error": err}), 400
    return jsonify({"ok": True, "message": "User added"})


@admin_bp.route("/users/<int:user_id>", methods=["DELETE"])
def remove_user(user_id):
    if not require_admin():
        return jsonify({"ok": False, "error": "Admin only"}), 403
    ok, err = delete_user(user_id)
    if not ok:
        return jsonify({"ok": False, "error": err}), 400
    return jsonify({"ok": True, "message": "User deleted"})


@admin_bp.route("/users/<int:user_id>", methods=["PUT"])
def change_user_password(user_id):
    if not require_admin():
        return jsonify({"ok": False, "error": "Admin only"}), 403
    data = request.get_json() or {}
    password = data.get("password") or ""
    ok, err = update_user_password(user_id, password)
    if not ok:
        return jsonify({"ok": False, "error": err}), 400
    return jsonify({"ok": True, "message": "Password updated"})


@admin_bp.route("/users/clear", methods=["POST"])
def clear_users():
    """Delete all users except admin."""
    if not require_admin():
        return jsonify({"ok": False, "error": "Admin only"}), 403
    n = clear_users_except_admin()
    return jsonify({"ok": True, "message": f"Removed {n} user(s). Admin kept."})
