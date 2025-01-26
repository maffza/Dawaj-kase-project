from django.db import connection

class PaymentManager:
    @staticmethod
    def donate(campaignID, userID, amount, message):
        with connection.cursor() as cursor:
            cursor.callproc("Crowdfunding_pkg.donate", [campaignID, userID, amount, message])

    @staticmethod
    def donate_anonymously(campaignID, amount, message):
        PaymentManager().donate(campaignID, 999999999, amount, message)