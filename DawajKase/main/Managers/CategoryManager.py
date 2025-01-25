from django.db import connection
import oracledb

class CategoryManager:
    @staticmethod
    def get_category_id_by_name(category_name):
        with connection.cursor() as cursor:
            ref_cursor = cursor.callfunc("Crowdfunding_pkg.get_category_id_by_name", oracledb.CURSOR,
				[category_name])
            result = ref_cursor.fetchone()
            if result:
                return result[0]
        return None