from django.db import connection
from ..Post import Post

class PostManager:
    @staticmethod
    def add_post(title, description, imagePath, userID, campaignID):
        with connection.cursor() as cursor:
            cursor.execute("INSERT INTO posts(title, description, image_url, user_id, campaign_id) VALUES (%s, %s, %s, %s, %s)",
                           [title, description, imagePath, userID, campaignID])

    @staticmethod 
    def get_posts(campaignID):
        posts = None
        with connection.cursor() as cursor:
            cursor.execute("SELECT id, title, description, image_url, user_id, campaign_id FROM posts WHERE campaign_id=%s ORDER BY creation_date DESC",
                           [campaignID])
            result = cursor.fetchall()

            posts = [Post(*p) for p in result]
        
        return posts