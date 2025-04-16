@echo off
python -m venv env
call env\Scripts\activate.bat
cd DawajKase
python manage.py runserver