from flask import Blueprint, request, jsonify, session

from auth_token import current_user_from_request
from db import get_all_users, create_user, delete_user, update_user_password, clear_users_except_admin, get_leaderboard
from timer_service import start_exam, pause_exam, reset_exam, get_status

admin_bp = Blueprint("admin", __name__, url_prefix="/api/admin")


def _admin_response():
    """Return (None, None) if OK, else (json_response, status_code). Uses Bearer token or session."""
    user = current_user_from_request(request, session)
    if not user:
        return jsonify({"ok": False, "error": "Login required", "code": "login_required"}), 401
    if not user.get("is_admin"):
        return jsonify({"ok": False, "error": "Admin only", "code": "admin_required"}), 403
    return None, None


@admin_bp.route("/start-exam", methods=["POST"])
def start_exam_route():
    err, status = _admin_response()
    if err is not None:
        return err, status
    start_exam()
    return jsonify({"ok": True, "message": "Exam timer started"})


@admin_bp.route("/pause-exam", methods=["POST"])
def pause_exam_route():
    err, status = _admin_response()
    if err is not None:
        return err, status
    pause_exam()
    return jsonify({"ok": True, "message": "Exam timer paused"})


@admin_bp.route("/reset-exam", methods=["POST"])
def reset_exam_route():
    err, status = _admin_response()
    if err is not None:
        return err, status
    reset_exam()
    return jsonify({"ok": True, "message": "Exam timer reset"})


@admin_bp.route("/timer-status", methods=["GET"])
def timer_status():
    err, status = _admin_response()
    if err is not None:
        return err, status
    return jsonify({"ok": True, **get_status()})


@admin_bp.route("/leaderboard", methods=["GET"])
def leaderboard():
    err, status = _admin_response()
    if err is not None:
        return err, status
    entries = get_leaderboard()
    return jsonify({"ok": True, "leaderboard": entries})


@admin_bp.route("/users", methods=["GET"])
def list_users():
    err, status = _admin_response()
    if err is not None:
        return err, status
    users = get_all_users()
    return jsonify({"ok": True, "users": users})


@admin_bp.route("/users", methods=["POST"])
def add_user():
    err, status = _admin_response()
    if err is not None:
        return err, status
    data = request.get_json() or {}
    username = (data.get("username") or "").strip()
    password = data.get("password") or ""
    ok, err = create_user(username, password)
    if not ok:
        return jsonify({"ok": False, "error": err}), 400
    return jsonify({"ok": True, "message": "User added"})


@admin_bp.route("/users/<int:user_id>", methods=["DELETE"])
def remove_user(user_id):
    err, status = _admin_response()
    if err is not None:
        return err, status
    ok, err = delete_user(user_id)
    if not ok:
        return jsonify({"ok": False, "error": err}), 400
    return jsonify({"ok": True, "message": "User deleted"})


@admin_bp.route("/users/<int:user_id>", methods=["PUT"])
def change_user_password(user_id):
    err, status = _admin_response()
    if err is not None:
        return err, status
    data = request.get_json() or {}
    password = data.get("password") or ""
    ok, err = update_user_password(user_id, password)
    if not ok:
        return jsonify({"ok": False, "error": err}), 400
    return jsonify({"ok": True, "message": "Password updated"})


@admin_bp.route("/users/clear", methods=["POST"])
def clear_users():
    """Delete all users except admin."""
    err, status = _admin_response()
    if err is not None:
        return err, status
    n = clear_users_except_admin()
    return jsonify({"ok": True, "message": f"Removed {n} user(s). Admin kept."})
