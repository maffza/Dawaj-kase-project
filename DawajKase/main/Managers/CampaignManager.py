
from django.db import connection
from ..Campaign import Campaign
from ..Donation import Donation
import oracledb

class CampaignManager:
    @staticmethod
    def get_campaigns_by_limit(amount, sort_by=None):
        campaigns = None
        query = "SELECT * FROM campaigns WHERE current_money_amount < target_money_amount"
        
        if sort_by == 'amount':
            query += " ORDER BY current_money_amount DESC"
        elif sort_by == 'time':
            query += " ORDER BY end_date ASC"
        elif sort_by == 'goal':
            query += " ORDER BY (target_money_amount - current_money_amount) ASC"
        else:
            query += " ORDER BY id DESC"
            
        query += " FETCH FIRST %s ROWS ONLY"

        with connection.cursor() as cursor:
            cursor.execute(query, [amount])
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

    @staticmethod
    def get_campaigns_sorted(sort_by=None, category_id=None):
        campaigns = []
        query = "SELECT c.* FROM campaigns c"

        if category_id:
            query += " WHERE c.category_id = %s"

        if sort_by == 'amount':
            query += " ORDER BY c.current_money_amount DESC"
        elif sort_by == 'time':
            query += " ORDER BY c.end_date ASC"
            
        with connection.cursor() as cursor:
            if category_id:
                cursor.execute(query, [category_id])
            else:
                cursor.execute(query)
            campaignsResult = cursor.fetchall()
            if campaignsResult:
                campaigns = [Campaign(*c).to_json() for c in campaignsResult]
                
        return campaigns

    @staticmethod
    def count_unique_donors(campaign_id):
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT COUNT(DISTINCT user_id) 
                FROM donations 
                WHERE campaign_id = %s AND user_id != 999999999
            """, [campaign_id])
            result = cursor.fetchone()
            return result[0] if result else 0

    @staticmethod
    def get_favourite_campaigns(user_id, sort_by=None):
        campaigns = []
        query = """
            SELECT c.* 
            FROM campaigns c
            JOIN favourites f ON c.id = f.campaign_id
            WHERE f.user_id = %s
        """
        
        if sort_by == 'amount':
            query += " ORDER BY c.current_money_amount DESC"
        elif sort_by == 'time':
            query += " ORDER BY c.end_date ASC"
            
        with connection.cursor() as cursor:
            cursor.execute(query, [user_id])
            campaignsResult = cursor.fetchall()
            if campaignsResult:
                campaigns = [Campaign(*c).to_json() for c in campaignsResult]
                
        return campaigns

    @staticmethod
    def get_favourite_campaigns_by_category(user_id, category_id, sort_by=None):
        campaigns = []
        query = """
            SELECT c.* 
            FROM campaigns c
            JOIN favourites f ON c.id = f.campaign_id
            WHERE f.user_id = %s AND c.category_id = %s
        """
        
        if sort_by == 'amount':
            query += " ORDER BY c.current_money_amount DESC"
        elif sort_by == 'time':
            query += " ORDER BY c.end_date ASC"
            
        with connection.cursor() as cursor:
            cursor.execute(query, [user_id, category_id])
            campaignsResult = cursor.fetchall()
            if campaignsResult:
                campaigns = [Campaign(*c).to_json() for c in campaignsResult]
                
        return campaigns
    def delete_campaign(campaign_id):
        pass
        #with connection.cursor() as cursor:
        #    cursor.execute("DELETE FROM campaigns WHERE id=%s", 
        #                        [campaign_id])
