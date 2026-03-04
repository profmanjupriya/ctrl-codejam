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

## Deploy backend to droplet (rsync)

Run **from inside the project directory** (so the source path is `.` or the current folder):

```bash
cd /path/to/ctrl-codejam
rsync -av --delete . root@64.23.188.213:/opt/ctrl-codejam/
```

- Use your real project path (e.g. `~/ctrl-codejam` or `~/Projects/ctrl-codejam`).  
- **Wrong:** `rsync ... ctrl-codejam/ ...` from your home directory — that looks for a folder named `ctrl-codejam` in `~` and fails with "No such file or directory" if you're not in it.

On the server after rsync:

```bash
cd /opt/ctrl-codejam/backend

# Build the code-runner Docker image (required for Run; Python/Java/C++ run inside it)
docker build -t codeblitz-runner:latest -f Dockerfile.runner .

python3 -m venv venv && source venv/bin/activate
pip install -r requirements.txt
# Ensure .env exists (ADMIN_USERNAME, ADMIN_DEFAULT_PASSWORD, CORS_ORIGINS, etc.)
python app.py
```

**"pull access denied" / "Unable to find image codeblitz-runner"** — The image must exist on the **same machine and same Docker** that runs the Flask app. Do this:

1. **SSH to the droplet** (the host where the app runs).
2. **Build there:** `cd /opt/ctrl-codejam/backend && docker build -t codeblitz-runner:latest -f Dockerfile.runner .`
3. **Confirm:** `docker images` should list `codeblitz-runner` with tag `latest`.
4. **Start (or restart) the app in that same environment** — e.g. in the same SSH session, or ensure systemd/cron runs as a user that can see that Docker (e.g. root). If you start the app in one terminal and built in another, both must be on the same server; if the app runs in a container, the image must be on the host that the app’s container uses for `docker run`.

**403 or 401 on admin routes (timer-status, add user, etc.):** The browser only sends the session cookie when the frontend and backend are the same site. If the frontend is at `http://localhost:5173` and the backend at `http://64.23.188.213:5000`, the cookie is **not** sent (cross-origin), so the server sees no session and returns **401** (or 403). Fix by using an **SSH tunnel** so the API is also on localhost:

1. **Open a tunnel** (leave this terminal open):
   ```bash
   ssh -L 5000:127.0.0.1:5000 root@64.23.188.213
   ```
   Now `http://localhost:5000` on your Mac is forwarded to the backend on the droplet.

2. **Point the frontend at localhost:** In `frontend/.env.local` set:
   ```bash
   VITE_API_BASE_URL=http://localhost:5000
   ```

3. **Run the frontend locally:** `cd frontend && npm run dev`, then open **http://localhost:5173** in the browser.

4. **Log in as admin.** The login request goes to localhost:5000 (tunnel → droplet). The cookie is set for localhost, so all later admin requests from the same page send the cookie and succeed.

- If you see **401** on admin routes, the session cookie is not being sent (check tunnel is open and you use `http://localhost:5173` and `VITE_API_BASE_URL=http://localhost:5000`).
- Server `.env`: default `CORS_ORIGINS` already includes `http://localhost:5173`. For a deployed frontend on another host (e.g. Vercel), add that URL to `CORS_ORIGINS` and, for cross-origin cookies over HTTPS, set `SESSION_COOKIE_SAMESITE=None` and `SESSION_COOKIE_SECURE=true` (backend must be HTTPS).

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
