CREATE OR REPLACE PACKAGE Crowdfunding_pkg AS

    FUNCTION get_comments_by_campaign_id(p_campaign_id IN NUMBER) RETURN SYS_REFCURSOR;
    
END Crowdfunding_pkg;
/

CREATE OR REPLACE PACKAGE BODY Crowdfunding_pkg AS

    FUNCTION get_comments_by_campaign_id(p_campaign_id IN NUMBER) 
    RETURN SYS_REFCURSOR IS
        result_cursor SYS_REFCURSOR;

    BEGIN
        OPEN result_cursor FOR
            SELECT 
                c.id AS comment_id,
                c.comment_text,
                c.creation_date,
                c.modify_date,
                u.first_name || ' ' || u.last_name AS username
            FROM 
                comments c
            JOIN 
                users u 
            ON 
                c.user_id = u.id
            WHERE 
                c.campaign_id = p_campaign_id
            ORDER BY 
                c.id DESC;

        RETURN result_cursor;
    END get_comments_by_campaign_id;

END Crowdfunding_pkg;
/
