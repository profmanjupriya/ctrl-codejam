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
        "starter_java": "public class Main {\n    public static void main(String[] args) {\n        for (int i = 0; i < 5; i++) {\n            System.out.println(i);\n        }\n    }\n}",
        "starter_cpp": "#include <iostream>\nusing namespace std;\n\nint main() {\n    for (int i = 0; i < 5; i++) {\n        cout << i << endl;\n    }\n    return 0;\n}",
        "expected": "0\n1\n2\n3\n4\n",
    },
    {
        "id": 1,
        "prompt": "Question 2: Print numbers 1 to 5",
        "starter": "for i in range(1, 6):\n    print(i)",
        "starter_java": "public class Main {\n    public static void main(String[] args) {\n        for (int i = 1; i <= 5; i++) {\n            System.out.println(i);\n        }\n    }\n}",
        "starter_cpp": "#include <iostream>\nusing namespace std;\n\nint main() {\n    for (int i = 1; i <= 5; i++) {\n        cout << i << endl;\n    }\n    return 0;\n}",
        "expected": "1\n2\n3\n4\n5\n",
    },
    {
        "id": 2,
        "prompt": "Question 3: Print 'Hello' 3 times",
        "starter": "for i in range(3):\n    print('Hello')",
        "starter_java": "public class Main {\n    public static void main(String[] args) {\n        for (int i = 0; i < 3; i++) {\n            System.out.println(\"Hello\");\n        }\n    }\n}",
        "starter_cpp": "#include <iostream>\nusing namespace std;\n\nint main() {\n    for (int i = 0; i < 3; i++) {\n        cout << \"Hello\" << endl;\n    }\n    return 0;\n}",
        "expected": "Hello\nHello\nHello\n",
    },
]
