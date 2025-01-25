from django.db import connection

class CategoryManager:
    @staticmethod
    def get_category_id_by_name(category_name):
        with connection.cursor() as cursor:
            cursor.execute("SELECT id FROM categories WHERE name = %s", [category_name])
            result = cursor.fetchone()
            if result:
                return result[0]
        return None