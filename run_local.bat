@echo off
setlocal
cd /d "%~dp0"

python manage.py runserver 0.0.0.0:8080 %*
endlocal
