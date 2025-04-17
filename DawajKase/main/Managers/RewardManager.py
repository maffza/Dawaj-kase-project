from django.db import connection
from ..Tier import Tier

class RewardManager:
    @staticmethod
    def insert_tiers(amounts, descriptions, campaignID):
        data = [
            (description, int(amount), campaignID)
            for amount, description in zip(amounts, descriptions)
        ]

        with connection.cursor() as cursor:
            cursor.executemany("INSERT INTO rewards(description, amount_required, campaign_id) VALUES (%s, %s, %s)", data)

    @staticmethod
    def get_campaign_tiers(campaignID):
        tiers = None
        with connection.cursor() as cursor:
            cursor.execute("SELECT id, description, amount_required, campaign_id FROM rewards WHERE campaign_id=%s ORDER BY amount_required",
                           [campaignID])
            result = cursor.fetchall()

            tiers = [Tier(*t) for t in result]
        
        return tiers