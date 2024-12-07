from .UserManager import UserManager
from .CampaignManager import CampaignManager
from .CommentManager import CommentManager

class ManagerFactory:
    @staticmethod
    def get_user_manager():
        return UserManager()

    @staticmethod
    def get_campaign_manager():
        return CampaignManager()

    @staticmethod
    def get_comment_manager():
        return CommentManager()