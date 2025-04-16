@echo off
IF NOT EXIST "env" (
    python -m venv env
)
call env\Scripts\activate.bat
cd DawajKase
python manage.py runserver