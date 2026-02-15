# Code Blitz — Speed Coding Competition

A speed coding competition app: **Flask** backend and **React** (Vite) frontend. Students log in with credentials provided by an admin and complete timed coding questions.

---

## Prerequisites

- **Backend:** Python 3.9+ (3.10+ recommended)
- **Frontend:** Node.js 18+ and npm

---

## Backend setup (Flask)

1. **Go to the backend directory:**
   ```bash
   cd backend
   ```

2. **Create and activate a virtual environment:**
   ```bash
   python3 -m venv venv
   ```
   - **macOS/Linux:** `source venv/bin/activate`
   - **Windows:** `venv\Scripts\activate`

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the server:**
   ```bash
   python app.py
   ```
   - Backend runs at **http://localhost:5000**
   - Creates `users.db` and ensures an admin user (login: `admin` / `code`) on first run

---

## Frontend setup (React + Vite)

1. **Go to the frontend directory:**
   ```bash
   cd frontend
   ```

2. **Install dependencies:**
   ```bash
   npm install
   ```

3. **Start the dev server:**
   ```bash
   npm run dev
   ```
   - Frontend runs at **http://localhost:3000**
   - Vite proxies `/api` to the Flask backend (port 5000), so **run the backend first** for login and questions to work.

4. **Other scripts:**
   - `npm run build` — production build (output in `dist/`)
   - `npm run preview` — preview the production build locally

---

## Running the full app

1. **Terminal 1 — Backend:**
   ```bash
   cd backend
   source venv/bin/activate   # or venv\Scripts\activate on Windows
   python app.py
   ```

2. **Terminal 2 — Frontend:**
   ```bash
   cd frontend
   npm run dev
   ```

3. Open **http://localhost:3000** in your browser.

---

## Backend API (summary)

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST   | `/api/auth/login`     | Login (body: `username`, `password`) |
| GET    | `/api/auth/me`       | Current user (session) |
| POST   | `/api/auth/logout`   | Logout |
| GET    | `/api/timer/status`  | Exam timer remaining (students) |
| GET    | `/api/questions/`   | List questions (id, prompt, starter) |
| POST   | `/api/questions/run` | Run code (body: `code`, `question_index`) |
| POST   | `/api/admin/start-exam` | Start exam timer (admin) |
| GET    | `/api/admin/users`  | List users (admin) |
| POST   | `/api/admin/users`  | Add user (admin) |
| DELETE | `/api/admin/users/<id>` | Delete user (admin) |
| POST   | `/api/admin/users/clear` | Clear all users except admin (admin) |

**Default admin:** `admin` / `code`

---

## App flow

- **Landing page** — Single scrollable page: Home, About, Info (time & location), Committee. **Registration** in the nav goes to the login page.
- **Registration (login) page** — Students log in with credentials given by admin. Admin logs in with `admin` / `code`.
- **Admin** — Start exam timer, add/delete users, clear users (except admin).
- **Question (student)** — Wait for admin to start the timer; code in the editor, run, earn points; quiz ends when time is up or all questions are done.
