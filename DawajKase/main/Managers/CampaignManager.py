
from django.db import connection
from ..Campaign import Campaign
from ..Donation import Donation
import oracledb

class CampaignManager:
    @staticmethod
    def get_campaigns_by_limit(amount, sort_by=None): # looks like it's an unused function now
        campaigns = None
        
        with connection.cursor() as cursor:
            ref_cursor = cursor.callfunc("Crowdfunding_pkg.get_campaigns_by_limit", oracledb.CURSOR,
                                [amount])
            campaignsResult = ref_cursor.fetchall()

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
            ref_cursor = cursor.callfunc("Crowdfunding_pkg.search_campaigns", oracledb.CURSOR, [query])
            campaignsResult = ref_cursor.fetchall()

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
            ref_cursor = cursor.callfunc("Crowdfunding_pkg.get_donations", oracledb.CURSOR,
				[campaignID])
            donationsResult = ref_cursor.fetchall()
            if donationsResult:
                donations = [Donation(*d).to_json() for d in donationsResult]

        return donations
    
    @staticmethod
    def get_campaigns_to_be_approved():
        campaigns = None

        with connection.cursor() as cursor:
            ref_cursor = cursor.callfunc("Crowdfunding_pkg.get_campaigns_to_be_approved", oracledb.CURSOR)
            campaignsResult = ref_cursor.fetchall()

            if campaignsResult:
                campaigns = [Campaign(*c).to_json() for c in campaignsResult]

        return campaigns
    
    @staticmethod
    def approve_campaign(campaignID):
        with connection.cursor() as cursor:
            cursor.execute("UPDATE campaigns SET status='Active' WHERE id = %s", 
                    [campaignID])
    @staticmethod
    def get_category_id_by_name(category_name):
        with connection.cursor() as cursor:
            cursor.execute("SELECT id FROM categories WHERE name = %s", [category_name])
            result = cursor.fetchone()
            if result:
                return result[0]
        return None

    @staticmethod
    def get_campaigns_by_category(category_id, sort_by=None):
        campaigns = []
        query = """
            SELECT c.* 
            FROM campaigns c
            WHERE c.category_id = %s
        """
        
        if sort_by == 'amount':
            query += " ORDER BY c.current_money_amount DESC"
        elif sort_by == 'time':
            query += " ORDER BY c.end_date ASC"
            
        with connection.cursor() as cursor:
            cursor.execute(query, [category_id])
            campaignsResult = cursor.fetchall()
            if campaignsResult:
                campaigns = [Campaign(*c).to_json() for c in campaignsResult]
                
        return campaigns

    @staticmethod
    def get_campaigns_sorted(sort_by=None):
        campaigns = []
        query = "SELECT c.* FROM campaigns c"
        
        if sort_by == 'amount':
            query += " ORDER BY c.current_money_amount DESC"
        elif sort_by == 'time':
            query += " ORDER BY c.end_date ASC"
            
        with connection.cursor() as cursor:
            cursor.execute(query)
            campaignsResult = cursor.fetchall()
            if campaignsResult:
                campaigns = [Campaign(*c).to_json() for c in campaignsResult]
                
        return campaigns

    @staticmethod
    def count_unique_donors(campaign_id):
        with connection.cursor() as cursor:
            return int(cursor.callfunc("Crowdfunding_pkg.count_unique_donors", oracledb.DB_TYPE_NUMBER, [campaign_id]))

        return 0

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
