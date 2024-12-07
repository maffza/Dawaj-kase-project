from .UserManager import UserManager
from .CampaignManager import CampaignManager

class ManagerFactory:
    @staticmethod
    def get_user_manager():
        return UserManager()

    @staticmethod
    def get_campaign_manager():
        return CampaignManager()

    