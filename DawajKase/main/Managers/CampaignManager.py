
from django.db import connection
from ..Campaign import Campaign
from ..Donation import Donation
import oracledb

class CampaignManager:
    @staticmethod
    def get_campaigns_by_limit(amount):
        campaigns = None

        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM campaigns FETCH FIRST %s ROWS ONLY", [amount])
            campaignsResult = cursor.fetchall()

            if campaignsResult:
                campaigns = [Campaign(*c).to_json() for c in campaignsResult]

        return campaigns
    
    @staticmethod
    def get_campaign_by_id(id):
        campaign = None

        with connection.cursor() as cursor:
            ref_cursor = cursor.callfunc("Crowdfunding_pkg.get_campaign_by_id", oracledb.CURSOR, [int(id)])
            campaignResult = ref_cursor.fetchone()
            campaign = Campaign(*campaignResult)

        return campaign
    
    @staticmethod
    def search_campaigns(query):
        campaigns = None

        if query is None:
            return campaigns

        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM campaigns c WHERE LOWER(c.title) LIKE LOWER(%s) ORDER BY c.id DESC", [f"%{query}%"])
            campaignsResult = cursor.fetchall()

            if campaignsResult:
                campaigns = [Campaign(*c).to_json() for c in campaignsResult]

        return campaigns
    
    @staticmethod
    def insert_campaign(title, shortDescription, description, targetMoneyAmount, endDate, imageURL, organizerID, categoryID):
        with connection.cursor() as cursor:
            cursor.execute("INSERT INTO campaigns(title, short_description, description, current_money_amount, target_money_amount, end_date, image_url, organizer_id, category_id) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)", 
                        [title, shortDescription, description, 0, targetMoneyAmount, endDate, imageURL, organizerID, categoryID])
            
    @staticmethod
    def add_campaign_to_favourites(campaignID, userID):
        with connection.cursor() as cursor:
            cursor.execute("INSERT INTO favourites(user_id, campaign_id) VALUES (%s, %s)", 
                    [userID, campaignID])
            
    @staticmethod
    def is_favourited_by_user_with_id(campaignID, userID):
        with connection.cursor() as cursor:
            cursor.execute("SELECT id FROM favourites WHERE user_id=%s AND campaign_id=%s", 
                    [userID, campaignID])
            result = cursor.fetchall()
            if result:
                return True
            
        return False
    
    @staticmethod
    def remove_campaign_from_favourites(campaignID, userID):
        with connection.cursor() as cursor:
            cursor.execute("DELETE FROM favourites WHERE user_id=%s AND campaign_id=%s", 
                    [userID, campaignID])
            
    @staticmethod
    def get_donations(campaignID):
        donations = None
        with connection.cursor() as cursor:
            cursor.execute("SELECT d.id, d.amount, d.message, CASE WHEN d.user_id = 999999999 THEN 'Anonymous' ELSE u.first_name || ' ' || u.last_name END as username, d.creation_date FROM donations d JOIN users u ON d.user_id=u.id WHERE campaign_id=%s ORDER BY d.id DESC", 
                    [campaignID])
            donationsResult = cursor.fetchall()
            if donationsResult:
                donations = [Donation(*d).to_json() for d in donationsResult]

        return donations
    
    @staticmethod
    def get_campaigns_to_be_approved():
        campaigns = None

        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM campaigns WHERE status LIKE 'ToApprove'")
            campaignsResult = cursor.fetchall()

            if campaignsResult:
                campaigns = [Campaign(*c).to_json() for c in campaignsResult]

        return campaigns
    
    @staticmethod
    def approve_campaign(campaignID):
        with connection.cursor() as cursor:
            cursor.execute("UPDATE campaigns SET status='Active' WHERE id = %s", 
                    [campaignID])
