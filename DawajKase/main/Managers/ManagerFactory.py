from .UserManager import UserManager

class ManagerFactory:
    @staticmethod
    def get_user_manager():
        return UserManager()
