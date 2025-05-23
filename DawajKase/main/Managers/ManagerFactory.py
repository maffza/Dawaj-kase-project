from .UserManager import UserManager
from .CampaignManager import CampaignManager
from .CommentManager import CommentManager
from .PaymentManager import PaymentManager
from .FavouriteManager import FavouriteManager
from .CategoryManager import CategoryManager
from .PostManager import PostManager 
from .RewardManager import RewardManager

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
    
    @staticmethod
    def get_payment_manager():
        return PaymentManager()
    
    @staticmethod
    def get_favourite_manager():
        return FavouriteManager()
    
    @staticmethod
    def get_category_manager():
        return CategoryManager()
    
    @staticmethod
    def get_post_manager():
        return PostManager()
    
    @staticmethod
    def get_reward_manager():
        return RewardManager()