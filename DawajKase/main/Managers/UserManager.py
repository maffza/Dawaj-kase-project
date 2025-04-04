from django.db import connection
import hashlib
from ..User import User
import oracledb

class UserManager:
    @staticmethod
    def log_user_in(email, password):
        with connection.cursor() as cursor:
            cursor.execute("SELECT password_hash FROM users WHERE email=%s", [email])
            row = cursor.fetchone()

        if row:
            userPasswordHash = row[0]

            hashedPassword = hashlib.sha256(password.encode()).hexdigest()

            if hashedPassword == userPasswordHash:
                with connection.cursor() as cursor:
                    cursor.execute("SELECT id, first_name, last_name, email, profile_picture_url, role FROM users WHERE email=%s", [email])
                    row = cursor.fetchone()
                
                if row:
                    return ("OK", User(*row))
                else:
                    return ("UnexpectedError", None)
            else:
                return ("InvalidPassword", None)
        else:
            return ("InvalidEmail", None)
    
    @staticmethod
    def check_if_user_exists(email):
        with connection.cursor() as cursor:
            return cursor.callfunc("Crowdfunding_pkg.check_if_user_exists", oracledb.DB_TYPE_NUMBER, [email]) == 1 # yes, it's NUMBER in the database
            
        return False

    @staticmethod
    def register_user(firstName, lastName, email, password, city, address):
        hashedPassword = hashlib.sha256(password.encode()).hexdigest()

        with connection.cursor() as cursor:
            cursor.execute("INSERT INTO users(first_name, last_name, address, city, email, password_hash, role) VALUES (%s, %s, %s, %s, %s, %s, %s)", 
                           [firstName, lastName, address, city, email, hashedPassword, "Supporter"])
            
    @staticmethod
    def get_user_by_id(id):
        user = None

        with connection.cursor() as cursor:
            ref_cursor = cursor.callfunc("Crowdfunding_pkg.get_user_by_id", oracledb.CURSOR,
                                         [int(id)])
            userResult = ref_cursor.fetchone()

            if userResult:
                user = User(*userResult)

        return user
    
    @staticmethod
    def send_verification_request(userID, phoneNumber, bankNumber, documentPhoto):
        with connection.cursor() as cursor:
            cursor.execute("UPDATE users SET phone=%s, bank_account=%s, document_photo=%s, role='ToVerify' WHERE id = %s", 
                                [phoneNumber, bankNumber, documentPhoto, userID])

    @staticmethod
    def get_all_users():
        users = None

        with connection.cursor() as cursor:
            cursor.execute("SELECT id, first_name, last_name, email, profile_picture_url, role FROM users WHERE id != 999999999 AND role != 'Admin' ORDER BY id")
            usersResult = cursor.fetchall()

            if usersResult:
                users = [User(*d).to_json() for d in usersResult]

        return users
    
    @staticmethod
    def change_role(userID, role):
        with connection.cursor() as cursor:
            cursor.execute("UPDATE users SET role=%s WHERE id = %s", 
                                [role, userID])
            
    @staticmethod
    def delete_user(userID):
        with connection.cursor() as cursor:
            cursor.execute("DELETE FROM users WHERE id = %s", 
                                [userID])