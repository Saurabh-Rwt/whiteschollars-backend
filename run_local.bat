@echo off
setlocal
cd /d "%~dp0"

if exist ".venv\\Scripts\\activate.bat" call ".venv\\Scripts\\activate.bat"
if exist "venv\\Scripts\\activate.bat" call "venv\\Scripts\\activate.bat"

set "DJANGO_ENV=local"
set "USE_SQLITE=1"

python manage.py runserver %*
endlocal
