from django.db import connection
import hashlib

class User:
    def __init__(self, name, email):
        self.name = name
        self.email = email

class UserManager:
    @staticmethod
    def log_user_in(email, password):
        with connection.cursor() as cursor:
            cursor.execute("SELECT email, password_hash, first_name FROM users WHERE email=%s", [email])
            row = cursor.fetchone()

        if row:
            userEmail, userPasswordHash, userFirstName = row[0], row[1], row[2]

            hashedPassword = hashlib.sha256(password.encode()).hexdigest()

            if hashedPassword == userPasswordHash:
                return ("OK", User(userFirstName, userEmail))
            else:
                return ("InvalidPassword", None)
        else:
            return ("InvalidEmail", None)