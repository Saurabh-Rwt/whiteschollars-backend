#!/usr/bin/env bash
set -euo pipefail

# Usage:
#   ./refresh_backend.sh

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$SCRIPT_DIR"
VENV_DIR="${VENV_DIR:-/root/whiteenv}"
SERVICE_NAME="whitescholars-backend"

cd "$PROJECT_DIR"

export DJANGO_ENV=production
export DJANGO_SETTINGS_MODULE=myproject.settings

echo "==> Running migrations"
"$VENV_DIR/bin/python" manage.py migrate --noinput

echo "==> Collecting static files"
"$VENV_DIR/bin/python" manage.py collectstatic --noinput

echo "==> Restarting systemd service: $SERVICE_NAME"
sudo systemctl restart "$SERVICE_NAME"

echo "==> Service status"
sudo systemctl --no-pager -l status "$SERVICE_NAME"

echo "==> Done"
