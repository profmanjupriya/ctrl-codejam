# Code Blitz backend

Flask API for auth, questions, timer, and admin. Student code runs in an isolated Docker container (runner image).

## Build runner once (on the droplet)

The app runs submitted code inside the `codeblitz-runner` image. Build that image **once** on the server where the app runs (e.g. Ubuntu 24.04 droplet). You do **not** need to rebuild it on every app deploy.

**Option A — script (recommended):**

```bash
cd /opt/ctrl-codejam/backend
chmod +x scripts/build_runner.sh   # once, if needed
./scripts/build_runner.sh
```

**Option B — manual:**

```bash
cd /opt/ctrl-codejam/backend
docker build -t codeblitz-runner:latest -f Dockerfile.runner .
docker run --rm --network none codeblitz-runner:latest python3 -c "print(42)"
```

If the second command prints `42`, the image is ready. Restart the Flask app so it uses the new image.

## Run the app (after runner is built)

```bash
cd /opt/ctrl-codejam/backend
python3 -m venv venv && source venv/bin/activate
pip install -r requirements.txt
python app.py
```
