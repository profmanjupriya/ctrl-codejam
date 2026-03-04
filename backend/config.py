import os
import json
import random

SECRET_KEY = os.environ.get("SECRET_KEY", "dev-secret-change-in-production")
DATABASE = os.path.join(os.path.dirname(__file__), "users.db")
TIME_PER_QUESTION = 30 * 60  # 30 minutes in seconds
RUN_COOLDOWN = 3  # seconds

# Questions are loaded from a JSON file on the backend only.
_QUESTIONS_FILE = os.environ.get(
    "QUESTIONS_FILE",
    os.path.join(os.path.dirname(__file__), "questions.json"),
)

with open(_QUESTIONS_FILE, "r", encoding="utf-8") as f:
    _ALL_QUESTIONS = json.load(f)

# Number of questions to use in a given run (default 10).
_NUM_QUESTIONS = int(os.environ.get("NUM_QUESTIONS", "10"))

if len(_ALL_QUESTIONS) <= _NUM_QUESTIONS:
    QUESTIONS = _ALL_QUESTIONS
else:
    # Pick a random subset once at startup so all users see the same exam.
    QUESTIONS = random.sample(_ALL_QUESTIONS, _NUM_QUESTIONS)
