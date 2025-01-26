
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
            cursor.callproc("Crowdfunding_pkg.insert_campaign",
                        [title, shortDescription, description, int(targetMoneyAmount), endDate, imageURL, int(organizerID), int(categoryID)])
            
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
            cursor.callproc("Crowdfunding_pkg.approve_campaign", [campaignID])

    # it could be merged together with get_campaigns_sorted, 
    # to not break the DRY principle. It would also make its usage easier.
    @staticmethod
    def get_campaigns_by_category(category_id, sort_by=None):
        campaigns = []
        query = """
            SELECT c.* 
            FROM campaigns c
            WHERE c.category_id = %s AND status != 'ToApprove'
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
        query = "SELECT c.* FROM campaigns c WHERE status != 'ToApprove'"
        
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

    # Try moving it to FavouriteManager, it could be merged together with get_favourite_campaigns_by_category, 
    # to not break the DRY principle. It would also make its usage easier.
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

    # Try moving it to FavouriteManager
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
