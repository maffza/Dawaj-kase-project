from django.db import connection
from ..Comment import Comment
import oracledb

class CommentManager:
    @staticmethod
    def get_comments_by_project_id(campaignID):
        comments = None
        
        with connection.cursor() as cursor:
            ref_cursor = cursor.callfunc("Crowdfunding_pkg.get_comments_by_campaign_id", oracledb.CURSOR, [int(campaignID)])
            commentsResult = ref_cursor.fetchall()
            
            if commentsResult:
                comments = [Comment(*c).to_json() for c in commentsResult]

        return comments