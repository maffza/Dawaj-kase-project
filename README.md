# Dawaj kase project
 Projekt na Inżynierie oprogramowania

# How to launch the app
## Update the database password
In the file *DawajKase/DawajKase/settings.py* replace the database password with
the one you configured while setting up the database.

(This project is supposed to run only on a local machine.)

## Launching
Open a terminal, navigate to the main directory and execute the following commands:
>1. python -m venv env
>2. env\Scripts\activate

(Ensure that (env) appears at the beginning of your command prompt)
>3. pip install -r requirements.txt
>4. cd DawajKase
>5. python manage.py runserver
