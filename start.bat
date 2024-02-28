@echo off
REM Open Chrome
start chrome http://127.0.0.1:8000


REM Start Django development server
python manage.py runserver 0.0.0.0:8000

REM Keep the command prompt window open so you can see server output
pause