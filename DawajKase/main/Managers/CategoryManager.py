from django.db import connection
import oracledb

class CategoryManager:
    @staticmethod
    def get_category_id_by_name(category_name):
        with connection.cursor() as cursor:
            return cursor.callfunc("Crowdfunding_pkg.get_category_id_by_name", oracledb.DB_TYPE_NUMBER, [category_name])
        return None