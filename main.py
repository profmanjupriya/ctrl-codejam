import tkinter as tk
import sys
import io
import threading
import time
import sqlite3

BG_COLOR = "#FF7F7F"
TIME_PER_QUESTION = 10 * 60  # 10 minutes
RUN_COOLDOWN = 5  # seconds


QUESTIONS = [
    {
        "prompt": "Question 1: Print numbers 0 to 4",
        "starter": "for i in range(5):\n    print(i)",
        "expected": "0\n1\n2\n3\n4\n"
    },
    {
        "prompt": "Question 2: Print numbers 1 to 5",
        "starter": "for i in range(1, 6):\n    print(i)",
        "expected": "1\n2\n3\n4\n5\n"
    },
    {
        "prompt": "Question 3: Print 'Hello' 3 times",
        "starter": "for i in range(3):\n    print('Hello')",
        "expected": "Hello\nHello\nHello\n"
    }
]

# ---------- DATABASE ----------
def init_db():
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

def register_user(username, password):
    try:
        conn = sqlite3.connect("users.db")
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO users (username, password) VALUES (?, ?)",
            (username, password)
        )
        conn.commit()
        conn.close()
        return True
    except sqlite3.IntegrityError:
        return False

def check_login(username, password):
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    cursor.execute(
        "SELECT * FROM users WHERE username=? AND password=?",
        (username, password)
    )
    result = cursor.fetchone()
    conn.close()
    return result is not None

# ---------- MAIN APP ----------
class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Test App")
        self.geometry("900x600")
        self.configure(bg=BG_COLOR)
        self.current_frame = None
        self.show_login_page()

    def show_login_page(self):
        if self.current_frame:
            self.current_frame.destroy()
        self.current_frame = LoginPage(self)
        self.current_frame.pack(fill="both", expand=True)

    def show_question_page(self):
        if self.current_frame:
            self.current_frame.destroy()
        self.current_frame = QuestionPage(self)
        self.current_frame.pack(fill="both", expand=True)

# ---------- LOGIN PAGE ----------
class LoginPage(tk.Frame):
    def __init__(self, master):
        super().__init__(master, bg=BG_COLOR)

        # Center container
        container = tk.Frame(self, bg=BG_COLOR)
        container.place(relx=0.5, rely=0.5, anchor="center")

        title = tk.Label(
            container,
            text="Welcome",
            bg=BG_COLOR,
            fg="white",
            font=("Arial", 28, "bold")
        )
        title.pack(pady=(0, 20))

        tk.Label(
            container,
            text="Username",
            bg=BG_COLOR,
            fg="white",
            font=("Arial", 16)
        ).pack(anchor="w")

        self.username = tk.Entry(container, font=("Arial", 16), width=20)
        self.username.pack(pady=(0, 15))

        tk.Label(
            container,
            text="Password",
            bg=BG_COLOR,
            fg="white",
            font=("Arial", 16)
        ).pack(anchor="w")

        self.password = tk.Entry(container, show="*", font=("Arial", 16), width=20)
        self.password.pack(pady=(0, 25))

        btn_frame = tk.Frame(container, bg=BG_COLOR)
        btn_frame.pack()

        tk.Button(
            btn_frame,
            text="Login",
            font=("Arial", 14, "bold"),
            width=10,
            command=self.login
        ).pack(side="left", padx=10)

        tk.Button(
            btn_frame,
            text="Register",
            font=("Arial", 14, "bold"),
            width=10,
            command=self.register
        ).pack(side="right", padx=10)

        self.msg = tk.Label(
            container,
            text="",
            bg=BG_COLOR,
            fg="yellow",
            font=("Arial", 14)
        )
        self.msg.pack(pady=15)

    def login(self):
        if check_login(self.username.get(), self.password.get()):
            self.master.show_question_page()
        else:
            self.msg.config(text="❌ Invalid login")

    def register(self):
        if register_user(self.username.get(), self.password.get()):
            self.msg.config(text="✅ Registered! You can log in.")
        else:
            self.msg.config(text="⚠ Username already exists")

# ---------- QUESTION PAGE ----------
class QuestionPage(tk.Frame):
    def __init__(self, master):
        super().__init__(master, bg=BG_COLOR)

        self.score = 0
        self.q_index = 0
        self.remaining_time = TIME_PER_QUESTION
        self.timer_running = False
        self.running = False

        top = tk.Frame(self, bg=BG_COLOR)
        top.pack(fill="x", padx=20, pady=10)

        self.score_label = tk.Label(top, text="Score: 0", bg=BG_COLOR, fg="white", font=("Arial", 14, "bold"))
        self.score_label.pack(side="left")

        self.timer_label = tk.Label(top, text="⏱ 10:00", bg=BG_COLOR, fg="white", font=("Arial", 14, "bold"))
        self.timer_label.pack(side="right")

        self.question_label = tk.Label(self, bg=BG_COLOR, fg="white",
                                       font=("Arial", 18, "bold"), wraplength=800)
        self.question_label.pack(pady=5)

        btns = tk.Frame(self, bg=BG_COLOR)
        btns.pack(pady=5)

        self.run_btn = tk.Button(
            btns,
            text="▶ Run",
            bg="black",
            fg="white",
            width=10,
            command=self.run_code
        )
        self.run_btn.pack()

        main = tk.Frame(self, bg=BG_COLOR)
        main.pack(expand=True, fill="both", padx=20, pady=10)
        main.columnconfigure(0, weight=1)
        main.columnconfigure(1, weight=1)

        self.editor = tk.Text(main, bg="#1e1e1e", fg="white", font=("Consolas", 12))
        self.editor.grid(row=0, column=0, sticky="nsew", padx=(0, 10))

        self.output = tk.Text(main, bg="#111111", fg="lime",
                              font=("Consolas", 12), state="disabled")
        self.output.grid(row=0, column=1, sticky="nsew", padx=(10, 0))

        self.load_question()
        self.start_timer()

    def start_timer(self):
        self.remaining_time = TIME_PER_QUESTION
        self.timer_running = True
        self.update_timer()

    def update_timer(self):
        if not self.timer_running:
            return
        if self.remaining_time <= 0:
            self.timer_running = False
            self.advance_question(True)
            return
        self.remaining_time -= 1
        m, s = divmod(self.remaining_time, 60)
        self.timer_label.config(text=f"⏱ {m:02}:{s:02}")
        self.after(1000, self.update_timer)

    def run_code(self):
        if self.running:
            return

        self.running = True
        self.run_btn.config(state="disabled")  # 🔒 disable
        self.clear_output()

        threading.Thread(target=self.execute).start()

        # ⏳ re-enable after delay
        self.after(RUN_COOLDOWN * 1000, self.enable_run)

    def enable_run(self):
        self.run_btn.config(state="normal")

    def execute(self):
        code = self.editor.get("1.0", tk.END)
        old_stdout = sys.stdout
        sys.stdout = io.StringIO()
        try:
            exec(code, {})
            output = sys.stdout.getvalue()
        except Exception as e:
            output = f"Error:\n{e}"
        sys.stdout = old_stdout
        self.show_output(output)
        self.check_answer(output)
        self.running = False

    def check_answer(self, output):
        expected = QUESTIONS[self.q_index]["expected"]
        if output == expected:
            self.timer_running = False
            points = max(10, int((self.remaining_time / TIME_PER_QUESTION) * 100))
            self.score += points
            self.score_label.config(text=f"Score: {self.score}")
            self.show_output(f"\n✅ Correct! +{points} points\n")
            self.after(1500, self.advance_question)

    def load_question(self):
        q = QUESTIONS[self.q_index]
        self.question_label.config(text=q["prompt"])
        self.editor.delete("1.0", tk.END)
        self.editor.insert("1.0", q["starter"])
        self.clear_output()

    def advance_question(self, timeout=False):
        self.q_index += 1
        if self.q_index >= len(QUESTIONS):
            self.end_quiz()
            return
        self.load_question()
        self.start_timer()

    def end_quiz(self):
        self.question_label.config(text="🎉 Quiz Complete!")
        self.editor.delete("1.0", tk.END)
        self.show_output(f"\nFinal Score: {self.score}\n")
        self.timer_label.config(text="⏱ 00:00")

    def clear_output(self):
        self.output.config(state="normal")
        self.output.delete("1.0", tk.END)
        self.output.config(state="disabled")

    def show_output(self, text):
        self.output.after(0, lambda: self._append(text))

    def _append(self, text):
        self.output.config(state="normal")
        self.output.insert(tk.END, text)
        self.output.config(state="disabled")

# ---------- RUN ----------
if __name__ == "__main__":
    init_db()
    App().mainloop()
