from django.db import connection
from ..Campaign import Campaign

class CampaignManager:
    @staticmethod
    def get_campaigns_by_limit(amount):
        campaigns = None

        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM campaigns FETCH FIRST %s ROWS ONLY", [amount])
            campaignsResult = cursor.fetchall()

            campaigns = [Campaign(*c).to_json() for c in campaignsResult]

        return campaigns