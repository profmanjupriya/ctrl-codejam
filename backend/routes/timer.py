from flask import Blueprint, jsonify, session

from timer_service import get_start_time, get_status

timer_bp = Blueprint("timer", __name__, url_prefix="/api/timer")


@timer_bp.route("/status", methods=["GET"])
def status():
    if not session.get("username"):
        return jsonify({"ok": False, "error": "Login required"}), 401
    data = get_status()
    data["ok"] = True
    data["start_time"] = get_start_time()
    return jsonify(data)
