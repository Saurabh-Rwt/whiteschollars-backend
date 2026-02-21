@echo off
setlocal
cd /d "%~dp0"

set "DJANGO_ENV=local"
set "USE_SQLITE=1"

python manage.py runserver 0.0.0.0:8080 %*
endlocal
