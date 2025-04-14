from django.db import connection
import oracledb

from ..Category import Category

class CategoryManager:
    @staticmethod
    def get_category_id_by_name(category_name):
        with connection.cursor() as cursor:
            return cursor.callfunc("Crowdfunding_pkg.get_category_id_by_name", oracledb.DB_TYPE_NUMBER, [category_name])
        return None
    
    @staticmethod
    def get_all_categories():
        categories = None
        with connection.cursor() as cursor:
            cursor.execute("SELECT id, name, description FROM categories")
            result = cursor.fetchall()

            categories = [Category(*c) for c in result]
        
        return categories