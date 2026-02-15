import sys
import io
import time

from flask import Blueprint, request, jsonify, session

from config import QUESTIONS, TIME_PER_QUESTION
from timer_service import get_remaining, get_start_time

questions_bp = Blueprint("questions", __name__, url_prefix="/api/questions")


@questions_bp.route("/", methods=["GET"])
def list_questions():
    if not session.get("username"):
        return jsonify({"ok": False, "error": "Login required"}), 401
    # Return prompts and starter only; expected is used server-side for run
    out = [
        {"id": q["id"], "prompt": q["prompt"], "starter": q["starter"]}
        for q in QUESTIONS
    ]
    return jsonify({"ok": True, "questions": out})


@questions_bp.route("/run", methods=["POST"])
def run_code():
    if not session.get("username"):
        return jsonify({"ok": False, "error": "Login required"}), 401

    data = request.get_json() or {}
    code = data.get("code", "")
    question_index = data.get("question_index", 0)

    if question_index < 0 or question_index >= len(QUESTIONS):
        return jsonify({"ok": False, "error": "Invalid question index"}), 400

    # Execute code
    old_stdout = sys.stdout
    sys.stdout = io.StringIO()
    try:
        exec(code, {})
        output = sys.stdout.getvalue()
    except Exception as e:
        output = f"Error:\n{e}"
    sys.stdout = old_stdout

    expected = QUESTIONS[question_index]["expected"]
    correct = output == expected

    points = 0
    if correct:
        remaining = get_remaining()
        if remaining is not None:
            points = max(10, int((remaining / TIME_PER_QUESTION) * 100))

    return jsonify({
        "ok": True,
        "output": output,
        "correct": correct,
        "points": points,
    })
