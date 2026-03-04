#!/usr/bin/env bash
set -euo pipefail

IP="64.23.188.213"
REMOTE="/opt/ctrl-codejam"

echo "Syncing project to droplet..."

rsync -az --delete \
  --exclude ".git" \
  --exclude "backend/venv" \
  --exclude "backend/__pycache__" \
  --exclude "backend/.env" \
  --exclude "frontend/node_modules" \
  --exclude "frontend/dist" \
  ./ root@${IP}:${REMOTE}/

echo "Rebuilding backend on droplet..."

ssh root@${IP} '
  set -e
  cd /opt/ctrl-codejam/backend

  pkill -f "python.*app.py" || true

  rm -rf venv
  python3 -m venv venv
  source venv/bin/activate

  python -m pip install --upgrade pip setuptools wheel
  python -m pip install -r requirements.txt

  nohup python app.py > app.log 2>&1 &

  sleep 2
  echo "Backend running processes:"
  pgrep -af "python.*app.py" || true
  echo ""
  echo "Recent log output:"
  tail -n 30 app.log || true
'

echo "Deployment finished."
