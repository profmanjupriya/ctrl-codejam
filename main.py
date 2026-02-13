import tkinter as tk
import sys
import io
import threading
import time
import sqlite3


BG_COLOR = "#FF7F7F"
TIME_PER_QUESTION = 30 * 60  # 10 minutes
RUN_COOLDOWN = 3  # seconds
#GLOBAL_TIMER = RemoteTimerService("http://SERVER_IP:5000")


def format_time(seconds):
   if seconds is None:
       return "--:--"
   m, s = divmod(seconds, 60)
   return f"{m:02}:{s:02}"


class TimerService:
   def start_exam(self):
       raise NotImplementedError


   def get_start_time(self):
       raise NotImplementedError




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

def get_all_usernames():
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    cursor.execute("SELECT username FROM users ORDER BY username COLLATE NOCASE")
    rows = cursor.fetchall()
    conn.close()
    return [r[0] for r in rows]



# ---------- MAIN APP ----------
class App(tk.Tk):
   def __init__(self):
       super().__init__()
       self.title("Test App")
       self.geometry("900x600")
       self.configure(bg=SHELL_BG)


       self.shell = MainShell(self)
       self.pages = {
           "home": lambda: HomePage(self.shell.body),
           "info": lambda: InfoPage(self.shell.body, "Info"),
           "registration": lambda: RegPage(self.shell.body, "Registration"),
           "sponsors": lambda: SponsorsPage(self.shell.body, "Sponsors"),
           "committee": lambda: CommitteePage(self.shell.body, "Committee"),
       }


       self.show_page("home")  # start on homepage


   def show_page(self, key):
       page_factory = self.pages.get(key)
       if not page_factory:
           return
       self.shell.set_page(page_factory())


   # 🧪 DEV HOTKEY: start exam timer
       self.bind_all("<Control-s>", self.dev_start_exam)


   def dev_start_exam(self, event=None):
       print("🧪 DEV: Admin timer started")
       GLOBAL_TIMER.start_exam()

   def show_login_page(self):
       self.shell.set_page(LoginPage(self.shell.body))

   def show_admin_page(self):
       self.shell.set_page(AdminPage(self.shell.body))

   def show_question_page(self):
       self.shell.set_page(QuestionPage(self.shell.body))


NAV_BG = "#20C6C6"   # turquoise
SHELL_BG = "#070A12"


class MainShell(tk.Frame):
   def __init__(self, master):
       super().__init__(master, bg=SHELL_BG)
       self.pack(fill="both", expand=True)


       self.bg = tk.Canvas(self, highlightthickness=0, bd=0, bg=SHELL_BG)
       self.bg.pack(fill="both", expand=True)
       self.bg.bind("<Configure>", self._on_resize)


       # --- NAV BAR ---
       self.nav = tk.Frame(self.bg, bg=NAV_BG, height=55)
       self.nav.pack_propagate(False)
       self.nav_window = self.bg.create_window(0, 0, window=self.nav, anchor="nw")


       nav_inner = tk.Frame(self.nav, bg=NAV_BG)
       nav_inner.pack(fill="both", expand=True)


       items = [
           ("Home", "home"),
           ("Info", "info"),
           ("Registration", "registration"),
           ("Sponsors", "sponsors"),
           ("Committee", "committee"),
       ]


       # Create 7 columns:
       # spacer | btn | btn | btn | btn | btn | spacer
       nav_inner.columnconfigure(0, weight=1)
       nav_inner.columnconfigure(len(items) + 1, weight=1)


       for i in range(1, len(items) + 1):
           nav_inner.columnconfigure(i, weight=0)


       for i, (label, key) in enumerate(items, start=1):


           if key == "registration":
               cmd = master.show_login_page  # go to login page
           else:
               cmd = lambda k=key: master.show_page(k)


           b = tk.Button(
               nav_inner,
               text=label,
               bg=NAV_BG,
               fg="black",
               activebackground=NAV_BG,
               activeforeground="black",
               font=("Arial", 14, "bold"),
               bd=0,
               relief="flat",
               cursor="hand2",
               command=cmd
           )
           b.grid(row=0, column=i, padx=15, pady=10)


       # --- BODY (page content) ---
       self.body = tk.Frame(self.bg, bg=SHELL_BG)
       self.body_window = self.bg.create_window(0, 65, window=self.body, anchor="nw")


       self.current_page = None


   def _on_resize(self, event):
       """Resize canvas windows so the nav bar is visible and full width."""
       w = event.width
       h = event.height


       # Resize + position nav and body windows
       self.bg.coords(self.nav_window, 0, 0)
       self.bg.itemconfigure(self.nav_window, width=w, height=55)


       self.bg.coords(self.body_window, 0, 65)
       self.bg.itemconfigure(self.body_window, width=w, height=max(0, h - 65))


       # Redraw background behind everything
       self._draw_background(w, h)


   def set_page(self, page_frame: tk.Frame):
       if self.current_page:
           self.current_page.destroy()
       self.current_page = page_frame
       self.current_page.pack(in_=self.body, fill="both", expand=True)


   def _draw_background(self, w, h):
       self.bg.delete("bg")
       self.bg.create_rectangle(0, 0, w, h, fill=SHELL_BG, outline="", tags="bg")


       line_colors = ["#152038", "#0E1830", "#1A2B52"]
       step = 90
       for i in range(-h, w, step):
           c = line_colors[(i // step) % len(line_colors)]
           self.bg.create_line(i, 0, i + h, h, fill=c, width=2, tags="bg")


       for y in range(0, h, 60):
           for x in range(0, w, 60):
               self.bg.create_oval(x, y, x + 2, y + 2, fill="#0B1020", outline="", tags="bg")


       # Make sure background stays behind nav/body
       self.bg.tag_lower("bg")


# ---------- HOME PAGE ----------
class HomePage(tk.Frame):
   def __init__(self, master):
       super().__init__(master, bg=SHELL_BG)


       # --- Header (centered) ---
       header = tk.Frame(self, bg=SHELL_BG)
       header.pack(pady=(30, 10))


       tk.Label(
           header,
           text="Code Blitz",
           bg=SHELL_BG,
           fg="white",
           font=("Arial", 40, "bold")
       ).pack(pady=(25, 8))


       sub = tk.Frame(header, bg=SHELL_BG)
       sub.pack()


       tk.Label(sub, text="Hosted by ", bg=SHELL_BG, fg="white", font=("Arial", 18, "bold")).pack(side="left")
       tk.Label(sub, text="CTRL ", bg=SHELL_BG, fg="#B46CFF", font=("Arial", 18, "bold")).pack(side="left")
       tk.Label(sub, text="SDSU", bg=SHELL_BG, fg="#FF3B3B", font=("Arial", 18, "bold")).pack(side="left")

       # --- Cards container (centered) ---
       cards_wrapper = tk.Frame(self, bg=SHELL_BG)
       cards_wrapper.pack(pady=(25, 0))

       cards = tk.Frame(cards_wrapper, bg=SHELL_BG)
       cards.pack()

       # Force fixed spacing
       for i in range(3):
           cards.columnconfigure(i, weight=0)

       self._make_card(cards, 0, "About the Code Blitz", "Join us for a high speed coding competetion\n"
       "where groups of up to 3 will band together to fight \n"
       "for the chance to win $450! The fastest, most accurate competitors will win it all", "Learn More")
       self._make_card(cards, 1, "Time and Location", "Templo Mayor, March 21st \n 9am to 1pm", "Event Info")
       self._make_card(cards, 2, "Registration is Open", "Registration!", "Discord")


   def _make_card(self, parent, col, title, body, button_text):
       border = "#F0A500"
       card_bg = "#0B1020"


       card = tk.Frame(
           parent,
           bg=card_bg,
           highlightbackground=border,
           highlightthickness=2,
           bd=0,
           width=430,
           height=240
       )
       card.grid(row=0, column=col, padx=18, pady=10, sticky="n")
       card.grid_propagate(False)


       tk.Label(card, text=title, bg=card_bg, fg="white", font=("Arial", 18, "bold")).pack(pady=(18, 10))


       tk.Label(
           card,
           text=body,
           bg=card_bg,
           fg="white",
           font=("Arial", 12),
           wraplength=380,
           justify="left"
       ).pack(padx=22)


       tk.Button(
           card,
           text=button_text,
           bg="#B07A12",
           fg="white",
           activebackground="#C98914",
           activeforeground="white",
           font=("Arial", 13, "bold"),
           bd=0,
           relief="flat",
           padx=18,
           pady=8,
           cursor="hand2",
           command=lambda: None
       ).pack(pady=18)




class InfoPage(tk.Frame):
   def __init__(self, master, title):
       super().__init__(master, bg=SHELL_BG)
       tk.Label(
           self,
           text=title,
           bg=SHELL_BG,
           fg="white",
           font=("Arial", 36, "bold")
       ).pack(pady=80)


class RegPage(tk.Frame):
   def __init__(self, master, title):
       super().__init__(master, bg=SHELL_BG)
       tk.Label(
           self,
           text=title,
           bg=SHELL_BG,
           fg="white",
           font=("Arial", 36, "bold")
       ).pack(pady=80)


class SponsorsPage(tk.Frame):
   def __init__(self, master, title):
       super().__init__(master, bg=SHELL_BG)
       tk.Label(
           self,
           text=title,
           bg=SHELL_BG,
           fg="white",
           font=("Arial", 36, "bold")
       ).pack(pady=80)


class CommitteePage(tk.Frame):
   def __init__(self, master, title):
       super().__init__(master, bg=SHELL_BG)
       tk.Label(
           self,
           text=title,
           bg=SHELL_BG,
           fg="white",
           font=("Arial", 36, "bold")
       ).pack(pady=80)


# ---------- LOGIN PAGE ----------
class LoginPage(tk.Frame):
    def __init__(self, master):
        super().__init__(master, bg=BG_COLOR)

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

        tk.Label(container, text="Username", bg=BG_COLOR, fg="white", font=("Arial", 16)).pack(anchor="w")
        self.username = tk.Entry(container, font=("Arial", 16), width=20)
        self.username.pack(pady=(0, 15))

        tk.Label(container, text="Password", bg=BG_COLOR, fg="white", font=("Arial", 16)).pack(anchor="w")
        self.password = tk.Entry(container, show="*", font=("Arial", 16), width=20)
        self.password.pack(pady=(0, 25))

        btn_frame = tk.Frame(container, bg=BG_COLOR)
        btn_frame.pack()

        tk.Button(btn_frame, text="Login", font=("Arial", 14, "bold"), width=10, command=self.login)\
            .pack(side="left", padx=10)

        tk.Button(btn_frame, text="Register", font=("Arial", 14, "bold"), width=10, command=self.register)\
            .pack(side="right", padx=10)

        self.msg = tk.Label(container, text="", bg=BG_COLOR, fg="yellow", font=("Arial", 14))
        self.msg.pack(pady=15)

    def _app(self):
        # Always get the real App instance (root window), even when embedded in Shell frames
        return self.winfo_toplevel()

    def login(self):
        username = self.username.get().strip()
        password = self.password.get()

        app = self.winfo_toplevel()  # <-- important

        # 🔐 Hardcoded admin login
        if username == "admin" and password == "code":
            app.show_admin_page()
            return

        # 👤 Normal user login
        if check_login(username, password):
            app.show_question_page()
        else:
            self.msg.config(text="❌ Invalid login")

    def register(self):
        username = self.username.get().strip()
        password = self.password.get()

        if register_user(username, password):
            self.msg.config(text="✅ Registered! You can log in.")
        else:
            self.msg.config(text="⚠ Username already exists")



class LocalTimerService(TimerService):
   def __init__(self, duration):
       self.duration = duration
       self.start_time = None


   def start_exam(self):
       if self.start_time is None:
           self.start_time = time.time()


   def get_start_time(self):
       return self.start_time


   def get_remaining(self):
       if self.start_time is None:
           return None
       return max(0, int(self.duration - (time.time() - self.start_time)))




class RemoteTimerService(TimerService):
   def __init__(self, server_url):
       self.server_url = server_url


   #def start_exam(self):
    #   requests.get(f"{self.server_url}/start", timeout=1)


   #def get_remaining(self):
    #   r = requests.get(f"{self.server_url}/status", timeout=1).json()
     #  return r["remaining"] if r["started"] else None


GLOBAL_TIMER = LocalTimerService(TIME_PER_QUESTION)


   # ------ admin page -------
def start_exam():
    GLOBAL_TIMER.start_exam()


class AdminPage(tk.Frame):
   def __init__(self, master):
       super().__init__(master, bg=BG_COLOR)


       container = tk.Frame(self, bg=BG_COLOR)
       container.place(relx=0.5, rely=0.5, anchor="center")


       tk.Label(
           container,
           text="Admin Control Panel",
           bg=BG_COLOR,
           fg="white",
           font=("Arial", 28, "bold")
       ).pack(pady=(0, 30))


       tk.Button(
           container,
           text="Start Exam Timer",
           font=("Arial", 16, "bold"),
           width=18,
           command=start_exam
       ).pack(pady=10)


       # 🔍 Debug timer display
       self.timer_label = tk.Label(
           container,
           text="⏱ Waiting to start",
           bg=BG_COLOR,
           fg="yellow",
           font=("Arial", 16, "bold")
       )
       self.timer_label.pack(pady=20)


       self.update_debug_timer()


       # ---------- Registered Users List ----------
       users_section = tk.Frame(container, bg=BG_COLOR)
       users_section.pack(pady=(10, 0), fill="x")

       tk.Label(
           users_section,
           text="Registered Users",
           bg=BG_COLOR,
           fg="white",
           font=("Arial", 16, "bold")
       ).pack(anchor="w")

       list_frame = tk.Frame(users_section, bg=BG_COLOR)
       list_frame.pack(pady=8, fill="both", expand=True)

       self.user_listbox = tk.Listbox(
           list_frame,
           font=("Arial", 12),
           height=10,
           width=30
       )
       self.user_listbox.pack(side="left", fill="both", expand=True)

       scrollbar = tk.Scrollbar(list_frame, orient="vertical", command=self.user_listbox.yview)
       scrollbar.pack(side="right", fill="y")
       self.user_listbox.config(yscrollcommand=scrollbar.set)

       tk.Button(
           users_section,
           text="Refresh Users",
           font=("Arial", 12, "bold"),
           command=self.refresh_users
       ).pack(pady=(6, 0), anchor="w")

       self.refresh_users()


   def refresh_users(self):
        self.user_listbox.delete(0, tk.END)
        try:
            for name in get_all_usernames():
                self.user_listbox.insert(tk.END, name)
        except Exception as e:
            self.user_listbox.insert(tk.END, f"Error loading users: {e}")

   def _app(self):
       return self.winfo_toplevel()

   def update_debug_timer(self):
        remaining = GLOBAL_TIMER.get_remaining()

        if remaining is None:
            self.timer_label.config(text="⏱ Waiting to start")
        else:
            self.timer_label.config(
                text=f"⏱ Remaining: {format_time(remaining)}"
            )
        self.after(1000, self.update_debug_timer)






# ---------- QUESTION PAGE ----------
class QuestionPage(tk.Frame):
   def __init__(self, master):
       super().__init__(master, bg=BG_COLOR)


       self.question_start_time = None
       self.score = 0
       self.q_index = 0
       self.running = False


       top = tk.Frame(self, bg=BG_COLOR)
       top.pack(fill="x", padx=20, pady=10)


       self.score_label = tk.Label(top, text="Score: 0", bg=BG_COLOR, fg="white", font=("Arial", 14, "bold"))
       self.score_label.pack(side="left")


       self.timer_label = tk.Label(top, text="⏱ Waiting for admin…", bg=BG_COLOR, fg="white", font=("Arial", 14, "bold"))
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
       self.editor.config(state="disabled")  # initially locked


       self.output = tk.Text(main, bg="#111111", fg="lime", font=("Consolas", 12), state="disabled")
       self.output.grid(row=0, column=1, sticky="nsew", padx=(10, 0))


       self.load_question()


       # Start polling for admin to start the exam
       self.after(1000, self.wait_for_exam_start)


   # ------------------- Wait for admin -------------------
   def wait_for_exam_start(self):
       if GLOBAL_TIMER.get_start_time() is None:
           self.timer_label.config(text="⏱ Waiting for admin…")
           self.after(1000, self.wait_for_exam_start)
           return


       # Exam started — unlock UI
       self.editor.config(state="normal")
       self.run_btn.config(state="normal")


       # Start updating the timer
       self.update_timer()


   def update_timer(self):
       start = GLOBAL_TIMER.get_start_time()
       if start is None:
           self.timer_label.config(text="⏱ Waiting for admin…")
           self.after(1000, self.update_timer)
           return


       elapsed = time.time() - start
       remaining = max(0, TIME_PER_QUESTION - int(elapsed))


       m, s = divmod(remaining, 60)
       self.timer_label.config(text=f"⏱ {m:02}:{s:02}")


       if remaining <= 0:
           self.advance_question(timeout=True)
           return


       self.after(1000, self.update_timer)


   # ------------------- Run code -------------------
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


   def on_execution_complete(self, output):
           self.show_output(output)
           self.check_answer(output)
           self.running = False


   # ------------------- Check answer -------------------
   def check_answer(self, output):
       expected = QUESTIONS[self.q_index]["expected"]


       elapsed = time.time() - self.question_start_time
       remaining = max(0, TIME_PER_QUESTION - int(elapsed))


       points = max(10, int((remaining / TIME_PER_QUESTION) * 100))


       if output == expected:
           remaining_global = GLOBAL_TIMER.get_remaining() or 0
           points = max(10, int((remaining_global / TIME_PER_QUESTION) * 100))


           self.score += points
           self.score_label.config(text=f"Score: {self.score}")
           self.show_output(f"\n✅ Correct! +{points} points\n")


           self.after(1500, self.advance_question)


   # ------------------- Questions -------------------
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
       # UI already unlocked, timer continues from GLOBAL_TIMER
       self.update_timer()


   # ------------------- End quiz -------------------
   def end_quiz(self):
       self.question_label.config(text="🎉 Quiz Complete!")
       self.editor.delete("1.0", tk.END)
       self.show_output(f"\nFinal Score: {self.score}\n")
       self.timer_label.config(text="⏱ 00:00")


   # ------------------- Output -------------------
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
