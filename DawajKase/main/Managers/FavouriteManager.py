from django.db import connection
from ..Campaign import Campaign
import oracledb

class FavouriteManager:
    @staticmethod
    def add_campaign_to_favourites(campaignID, userID):
        with connection.cursor() as cursor:
            cursor.execute("INSERT INTO favourites(user_id, campaign_id) VALUES (%s, %s)", 
                    [userID, campaignID])
            
    @staticmethod
    def is_favourited_by_user_with_id(campaignID, userID):
        with connection.cursor() as cursor:
            return cursor.callfunc("Crowdfunding_pkg.is_favourited_by_user_with_id", oracledb.DB_TYPE_BOOLEAN, [campaignID, userID])
            
        return False
    
    @staticmethod
    def remove_campaign_from_favourites(campaignID, userID):
        with connection.cursor() as cursor:
            cursor.execute("DELETE FROM favourites WHERE user_id=%s AND campaign_id=%s", 
                    [userID, campaignID])
            
    @staticmethod
    def get_favourite_campaigns(userID, categoryID=None):
        campaigns = []
        query = "SELECT c.* FROM favourites f JOIN users u ON f.user_id=u.id JOIN campaigns c ON c.id=f.campaign_id WHERE u.id=%s"
        if categoryID:
            query += " AND c.category_id=%s"
        with connection.cursor() as cursor:
            if categoryID:
                cursor.execute(query, 
                            [userID, categoryID])
            else:
                cursor.execute(query, 
                        [userID])
            campaignsResult = cursor.fetchall()
            if campaignsResult:
                campaigns = [Campaign(*c).to_json() for c in campaignsResult]
                
        return campaigns