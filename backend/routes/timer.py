from flask import Blueprint, jsonify, session

from timer_service import get_remaining, get_start_time

timer_bp = Blueprint("timer", __name__, url_prefix="/api/timer")


@timer_bp.route("/status", methods=["GET"])
def status():
    if not session.get("username"):
        return jsonify({"ok": False, "error": "Login required"}), 401
    remaining = get_remaining()
    start = get_start_time()
    return jsonify({
        "ok": True,
        "started": start is not None,
        "remaining": remaining,
        "start_time": start,
    })
