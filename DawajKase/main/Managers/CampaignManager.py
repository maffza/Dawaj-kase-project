from django.db import connection
from ..Campaign import Campaign

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
    def get_campaigns_by_id(id):
        campaign = None

        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM campaigns WHERE id=%s", [id])
            campaignResult = cursor.fetchone()

            if campaignResult:
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
            cursor.execute("INSERT INTO campaigns(title, short_description, description, target_money_amount, end_date, image_url, organizer_id, category_id) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)", 
                        [title, shortDescription, description, targetMoneyAmount, endDate, imageURL, organizerID, categoryID])