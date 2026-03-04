import sys
import io
import os
import tempfile
import subprocess

from flask import Blueprint, request, jsonify, session

from config import QUESTIONS, TIME_PER_QUESTION
from db import record_score
from timer_service import get_remaining, get_start_time, get_status

questions_bp = Blueprint("questions", __name__, url_prefix="/api/questions")

RUN_TIMEOUT_SEC = 10
DOCKER_BIN = os.environ.get("DOCKER_BIN", "docker")
RUNNER_IMAGE = os.environ.get("RUNNER_IMAGE", "codeblitz-runner:latest")


def _run_in_docker(lang: str, code: str) -> str:
    """
    Execute untrusted code inside an isolated Docker container.

    - lang: 'python', 'java', or 'cpp'
    - code: source code string
    """
    with tempfile.TemporaryDirectory() as d:
        if lang == "python":
            src_name = "main.py"
            inner_cmd = ["python", "main.py"]
        elif lang == "java":
            src_name = "Main.java"
            # Compile then run Main
            inner_cmd = ["sh", "-lc", "javac Main.java && java Main"]
        else:  # cpp
            src_name = "solution.cpp"
            # Compile then run the binary
            inner_cmd = ["sh", "-lc", "g++ -o main solution.cpp && ./main"]

        src_path = os.path.join(d, src_name)
        with open(src_path, "w", encoding="utf-8") as f:
            f.write(code)

        cmd = [
            DOCKER_BIN,
            "run",
            "--rm",
            "--network",
            "none",
            "--memory",
            "512m",
            "--cpus",
            "0.5",
            "-v",
            f"{d}:/sandbox",
            "-w",
            "/sandbox",
            RUNNER_IMAGE,
        ] + inner_cmd

        try:
            proc = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=RUN_TIMEOUT_SEC,
            )
        except subprocess.TimeoutExpired:
            return f"Error:\nTimeout after {RUN_TIMEOUT_SEC}s"
        except FileNotFoundError:
            return "Error:\nDocker is not available on the judge server."

        out = proc.stdout or ""
        err = proc.stderr or ""

        if proc.returncode != 0:
            err_stripped = err.strip()
            # Missing image: user must build on the server (same host/user as the app)
            if "Unable to find image" in err_stripped or "pull access denied" in err_stripped or "repository does not exist" in err_stripped:
                return (
                    "Runtime Error:\n"
                    "The code-runner Docker image is missing on this server. "
                    "SSH to the server where the app runs and run:\n"
                    "  cd /opt/ctrl-codejam/backend && docker build -t codeblitz-runner:latest -f Dockerfile.runner .\n"
                    "Then restart the app. Ensure you build on the same machine (and same Docker) that runs the app."
                )
            if err_stripped:
                return f"Runtime Error:\n{err_stripped}"
            if out.strip():
                return out.strip()
            return f"Error:\nRunner exited with code {proc.returncode}"

        if err and not out:
            return err.strip()
        if err:
            return (out + "\n" + err).strip()
        return out.strip()


def run_python(code: str) -> str:
    return _run_in_docker("python", code)


def run_java(code: str) -> str:
    return _run_in_docker("java", code)


def run_cpp(code: str) -> str:
    return _run_in_docker("cpp", code)


@questions_bp.route("/", methods=["GET"])
def list_questions():
    if not session.get("username"):
        return jsonify({"ok": False, "error": "Login required"}), 401
    out = [
        {
            "id": q["id"],
            "prompt": q["prompt"],
            "starter": q["starter"],
            "starter_java": q.get("starter_java", q["starter"]),
            "starter_cpp": q.get("starter_cpp", q["starter"]),
        }
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
    language = (data.get("language") or "python").lower().strip()
    preview = data.get("preview", False)

    if question_index < 0 or question_index >= len(QUESTIONS):
        return jsonify({"ok": False, "error": "Invalid question index"}), 400

    if language not in ("python", "java", "cpp"):
        return jsonify({"ok": False, "error": "Invalid language. Use python, java, or cpp."}), 400

    if language == "python":
        output = run_python(code)
    elif language == "java":
        output = run_java(code)
    else:
        output = run_cpp(code)

    expected = QUESTIONS[question_index]["expected"]
    correct = output.strip() == expected.strip()

    points = 0
    if correct and not preview:
        remaining = get_remaining()
        if remaining is not None:
            points = max(10, int((remaining / TIME_PER_QUESTION) * 100))
        else:
            # Timer suspended: award fixed points per correct answer
            if get_status().get("suspended"):
                points = 10
        if points > 0:
            user_id = session.get("user_id")
            if user_id:
                record_score(user_id, points)

    return jsonify({
        "ok": True,
        "output": output,
        "correct": correct,
        "points": points,
        "preview": preview,
    })
