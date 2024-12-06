# Dawaj kase project
 Projekt na Inżynierie oprogramowania

# How to set up the project
## Update the database password
Create a file named *"secrets.json"* in the directory *DawajKase/DawajKase/*, and put the following content inside it:
```
{
    "DATABASE_PASSWORD": "YOUR_PASSWORD"
}
```

Replace *YOUR_PASSWORD* with the password that you configured while setting up the database.

(This project is supposed to run only on a local machine.)

## Setting up and running
Open a terminal, navigate to the main directory and execute the following commands:
>1. python -m venv env
>2. env\Scripts\activate

(Ensure that (env) appears at the beginning of your command prompt)
>3. pip install -r requirements.txt
>4. cd DawajKase
>5. python manage.py migrate
>6. python manage.py runserver

## Running
Each time after opening a new terminal, execute the following commands to run the project:
>1. env\Scripts\activate
>2. cd DawajKase
>3. python manage.py runserver