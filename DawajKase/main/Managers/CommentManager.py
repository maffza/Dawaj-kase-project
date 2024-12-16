from django.db import connection
from ..Comment import Comment
import cx_Oracle

class CommentManager:
    @staticmethod
    def get_comments_by_project_id(campaignID):
        comments = None
        
        with connection.cursor() as cursor:
            cursor.execute("SELECT c.id, c.comment_text, c.creation_date, c.modify_date, u.first_name || ' ' || u.last_name AS username FROM comments c JOIN users u ON c.user_id=u.id WHERE c.campaign_id=%s ORDER BY c.id DESC;", [campaignID])
            #result_cursor = cursor.var(cx_Oracle.CURSOR)
            
            #cursor.callproc("Crowdfunding_pkg.get_comments_by_campaign_id", [campaignID, result_cursor])
            
            #ref_cursor = result_cursor.getvalue()
            commentsResult = cursor.fetchall()
            
            if commentsResult:
                comments = [Comment(*c).to_json() for c in commentsResult]

        return comments