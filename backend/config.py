import os

SECRET_KEY = os.environ.get("SECRET_KEY", "dev-secret-change-in-production")
DATABASE = os.path.join(os.path.dirname(__file__), "users.db")
TIME_PER_QUESTION = 30 * 60  # 30 minutes in seconds
RUN_COOLDOWN = 3  # seconds

QUESTIONS = [
    {
        "id": 0,
        "prompt": "Question 1: Print numbers 0 to 4",
        "starter": "for i in range(5):\n    print(i)",
        "expected": "0\n1\n2\n3\n4\n",
    },
    {
        "id": 1,
        "prompt": "Question 2: Print numbers 1 to 5",
        "starter": "for i in range(1, 6):\n    print(i)",
        "expected": "1\n2\n3\n4\n5\n",
    },
    {
        "id": 2,
        "prompt": "Question 3: Print 'Hello' 3 times",
        "starter": "for i in range(3):\n    print('Hello')",
        "expected": "Hello\nHello\nHello\n",
    },
]
