#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

export DJANGO_ENV="${DJANGO_ENV:-production}"
export DJANGO_SETTINGS_MODULE="${DJANGO_SETTINGS_MODULE:-myproject.settings}"

python manage.py migrate --noinput
python manage.py collectstatic --noinput

exec gunicorn myproject.wsgi:application \
  --bind "0.0.0.0:${PORT:-8000}" \
  --workers "${GUNICORN_WORKERS:-3}" \
  --timeout "${GUNICORN_TIMEOUT:-120}" \
  "$@"
