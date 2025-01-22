from django.db import connection

class PaymentManager:
    @staticmethod
    def donate(campaignID, userID, amount, message):
        with connection.cursor() as cursor:
            cursor.execute("UPDATE campaigns SET CURRENT_MONEY_AMOUNT = CURRENT_MONEY_AMOUNT + %s WHERE id = %s", 
                    [amount, campaignID])

        with connection.cursor() as cursor:
            cursor.execute("INSERT INTO donations(amount, message, campaign_id, user_id) VALUES (%s, %s, %s, %s)", 
                    [amount, message, campaignID, userID])

    @staticmethod
    def donate_anonymously(campaignID, amount, message):
        PaymentManager().donate(campaignID, 999999999, amount, message)