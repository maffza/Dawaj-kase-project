CREATE OR REPLACE PACKAGE Crowdfunding_pkg AS

    FUNCTION get_comments_by_campaign_id(p_campaign_id IN NUMBER) RETURN SYS_REFCURSOR;
    FUNCTION get_campaigns_by_limit (p_amount IN NUMBER, p_sort_by IN VARCHAR2 DEFAULT NULL) RETURN SYS_REFCURSOR;
    FUNCTION search_campaigns (p_query IN VARCHAR2) RETURN SYS_REFCURSOR;
    PROCEDURE insert_campaign (p_title IN VARCHAR2, p_short_description IN VARCHAR2, p_description IN CLOB,
                            p_target_money_amount IN NUMBER, p_end_date IN DATE, p_image_url IN VARCHAR2,
                            p_organizer_id IN NUMBER, p_category_id IN NUMBER);
    PROCEDURE add_campaign_to_favourites (p_campaign_id IN NUMBER, p_user_id IN NUMBER);
    FUNCTION is_favourited_by_user_with_id (p_campaign_id IN NUMBER, p_user_id IN NUMBER) RETURN BOOLEAN;
    PROCEDURE remove_campaign_from_favourites (p_campaign_id IN NUMBER , p_user_id IN NUMBER);
    FUNCTION get_donations (p_campaign_id IN NUMBER) RETURN SYS_REFCURSOR;
    FUNCTION get_campaigns_to_be_approved RETURN SYS_REFCURSOR;
    PROCEDURE approve_campaign (p_campaign_id IN NUMBER);
    FUNCTION get_category_id_by_name (p_category_name IN VARCHAR2) RETURN NUMBER;
    FUNCTION get_campaigns_by_category (p_category_id IN NUMBER, p_sort_by IN VARCHAR2 DEFAULT NULL) RETURN SYS_REFCURSOR;
    FUNCTION get_campaigns_sorted (p_sort_by IN VARCHAR2 DEFAULT NULL) RETURN SYS_REFCURSOR;
    FUNCTION count_unique_donors (p_campaign_id IN NUMBER) RETURN NUMBER;
    PROCEDURE donate (p_campaign_id IN NUMBER, p_user_id IN NUMBER, p_amount IN NUMBER, p_message IN VARCHAR2);
    PROCEDURE donate_anonymously (p_campaign_id IN NUMBER, p_amount IN NUMBER, p_message IN VARCHAR2);
    FUNCTION check_if_user_exists (p_email IN VARCHAR2) RETURN NUMBER;
    FUNCTION get_user_by_id (p_id IN NUMBER) RETURN SYS_REFCURSOR;
    PROCEDURE reject_campaign (p_campaign_id IN NUMBER);
    FUNCTION get_successful_campaigns (p_start_date DATE, p_end_date DATE) RETURN SYS_REFCURSOR;
    FUNCTION get_verified_user_campaigns RETURN SYS_REFCURSOR;
    -- BRAK register_user
    -- BRAK log_user_in
    
END Crowdfunding_pkg;
/

CREATE OR REPLACE PACKAGE BODY Crowdfunding_pkg AS

    FUNCTION get_comments_by_campaign_id(p_campaign_id IN NUMBER) RETURN SYS_REFCURSOR
    IS
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

    FUNCTION get_campaigns_by_limit (p_amount IN NUMBER, p_sort_by IN VARCHAR2 DEFAULT NULL) RETURN SYS_REFCURSOR
    IS
        result_cursor SYS_REFCURSOR;
        v_query       VARCHAR2(4000);
    BEGIN
        v_query := 'SELECT * FROM campaigns WHERE current_money_amount < target_money_amount';

        IF p_sort_by = 'amount' THEN
            v_query := v_query || ' ORDER BY current_money_amount DESC';
        ELSIF p_sort_by = 'time' THEN
            v_query := v_query || ' ORDER BY end_date ASC';
        ELSIF p_sort_by = 'goal' THEN
            v_query := v_query || ' ORDER BY (target_money_amount - current_money_amount) ASC';
        ELSE
            v_query := v_query || ' ORDER BY id DESC';
        END IF;

        v_query := v_query || ' FETCH FIRST :1 ROWS ONLY';

        OPEN result_cursor FOR v_query USING p_amount;

        RETURN result_cursor;
    END get_campaigns_by_limit;
    
    FUNCTION search_campaigns (p_query IN VARCHAR2) RETURN SYS_REFCURSOR
    IS
        result_cursor SYS_REFCURSOR;
    BEGIN
        IF p_query IS NULL THEN
            RETURN NULL;
        END IF;

        OPEN result_cursor FOR
            SELECT *
            FROM campaigns c
            WHERE LOWER(c.title) LIKE LOWER('%' || p_query || '%')
            ORDER BY c.id DESC;

        RETURN result_cursor;
    END search_campaigns;
    
    PROCEDURE insert_campaign (p_title IN VARCHAR2, p_short_description IN VARCHAR2, p_description IN CLOB,
                            p_target_money_amount IN NUMBER, p_end_date IN DATE, p_image_url IN VARCHAR2,
                            p_organizer_id IN NUMBER, p_category_id IN NUMBER)
    IS
    
    BEGIN
        INSERT INTO campaigns (title, short_description, description, current_money_amount, target_money_amount, 
        end_date, image_url, organizer_id, category_id) 
        VALUES (p_title, p_short_description, p_description, 0, p_target_money_amount, p_end_date, 
        p_image_url, p_organizer_id, p_category_id);
    END insert_campaign;
    
    PROCEDURE add_campaign_to_favourites (p_campaign_id IN NUMBER, p_user_id IN NUMBER)
    IS
    
    BEGIN
        INSERT INTO favourites (user_id, campaign_id) 
        VALUES (p_user_id, p_campaign_id);
    END add_campaign_to_favourites;
    
    FUNCTION is_favourited_by_user_with_id (p_campaign_id IN NUMBER, p_user_id IN NUMBER) RETURN BOOLEAN
    IS
        v_count NUMBER;
    BEGIN
        SELECT COUNT(*)
        INTO v_count
        FROM favourites
        WHERE user_id = p_user_id
        AND campaign_id = p_campaign_id;

        RETURN v_count > 0;
    END is_favourited_by_user_with_id;
    
    PROCEDURE remove_campaign_from_favourites (p_campaign_id IN NUMBER ,p_user_id IN NUMBER)
    IS

    BEGIN
        DELETE FROM favourites
        WHERE user_id = p_user_id
        AND campaign_id = p_campaign_id;
    END remove_campaign_from_favourites;
    
    FUNCTION get_donations (p_campaign_id IN NUMBER) RETURN SYS_REFCURSOR
    IS
        result_cursor SYS_REFCURSOR;
    BEGIN
        OPEN result_cursor FOR
            SELECT d.id, d.amount, d.message,
               CASE
                   WHEN d.user_id = 999999999 THEN 'Anonymous'
                   ELSE u.first_name || ' ' || u.last_name
               END AS username,
               d.creation_date
        FROM donations d
        LEFT JOIN users u ON d.user_id = u.id
        WHERE d.campaign_id = p_campaign_id
        ORDER BY d.id DESC;

        RETURN result_cursor;
    END get_donations;
    
    FUNCTION get_campaigns_to_be_approved RETURN SYS_REFCURSOR
    IS
        result_cursor SYS_REFCURSOR;
    BEGIN
        OPEN result_cursor FOR
            SELECT *
            FROM campaigns
            WHERE status LIKE 'ToApprove';

        RETURN result_cursor;
    END get_campaigns_to_be_approved;

    PROCEDURE approve_campaign (p_campaign_id IN NUMBER)
    IS
    
    BEGIN
        UPDATE campaigns
        SET status = 'Active'
        WHERE id = p_campaign_id;
    END approve_campaign;
    
    FUNCTION get_category_id_by_name (p_category_name IN VARCHAR2) RETURN NUMBER
    IS
    v_category_id NUMBER;
    BEGIN
        SELECT id
        INTO v_category_id
        FROM categories
        WHERE name = p_category_name;

        RETURN v_category_id;

    EXCEPTION WHEN NO_DATA_FOUND THEN
        RETURN NULL;
    END get_category_id_by_name;
    
    FUNCTION get_campaigns_by_category (p_category_id IN NUMBER, p_sort_by IN VARCHAR2 DEFAULT NULL) RETURN SYS_REFCURSOR
    IS
        result_cursor SYS_REFCURSOR;
    BEGIN
        IF p_sort_by = 'amount' THEN
            OPEN result_cursor FOR
                SELECT c.*
                FROM campaigns c
                WHERE c.category_id = p_category_id
                ORDER BY c.current_money_amount DESC;
        ELSIF p_sort_by = 'time' THEN
            OPEN result_cursor FOR
                SELECT c.*
                FROM campaigns c
                WHERE c.category_id = p_category_id
                ORDER BY c.end_date ASC;
        ELSE
            OPEN result_cursor FOR
                SELECT c.*
                FROM campaigns c
                WHERE c.category_id = p_category_id;
        END IF;

        RETURN result_cursor;
    END get_campaigns_by_category;
    
    FUNCTION get_campaigns_sorted (p_sort_by IN VARCHAR2 DEFAULT NULL) RETURN SYS_REFCURSOR
    IS
        result_cursor SYS_REFCURSOR;
    BEGIN
        IF p_sort_by = 'amount' THEN
            OPEN result_cursor FOR
                SELECT c.*
                FROM campaigns c
                ORDER BY c.current_money_amount DESC;
        ELSIF p_sort_by = 'time' THEN
            OPEN result_cursor FOR
                SELECT c.*
                FROM campaigns c
                ORDER BY c.end_date ASC;
        ELSE
            OPEN result_cursor FOR
                SELECT c.*
                FROM campaigns c;
        END IF;

        RETURN result_cursor;
    END get_campaigns_sorted;
    
    FUNCTION count_unique_donors (p_campaign_id IN NUMBER) RETURN NUMBER
    IS
        v_donor_count NUMBER;
    BEGIN
        SELECT COUNT(DISTINCT user_id)
        INTO v_donor_count
        FROM donations
        WHERE campaign_id = p_campaign_id
        AND user_id != 999999999;

        RETURN v_donor_count;

    EXCEPTION WHEN NO_DATA_FOUND THEN
        RETURN 0;
    END count_unique_donors;
    
    PROCEDURE donate (p_campaign_id IN NUMBER, p_user_id IN NUMBER, p_amount IN NUMBER, p_message IN VARCHAR2)
    IS
    
    BEGIN
        UPDATE campaigns
        SET current_money_amount = current_money_amount + p_amount
        WHERE id = p_campaign_id;

        INSERT INTO donations (amount, message, campaign_id, user_id)
        VALUES (p_amount, p_message, p_campaign_id, p_user_id);

        COMMIT;
    END donate;
    
    PROCEDURE donate_anonymously (p_campaign_id IN NUMBER, p_amount IN NUMBER, p_message IN VARCHAR2)
    IS
    
    BEGIN
        donate(p_campaign_id, 999999999, p_amount, p_message);
    END donate_anonymously;
    
    FUNCTION check_if_user_exists (p_email IN VARCHAR2) RETURN NUMBER
    IS
        v_exists NUMBER := 0;
    BEGIN
        SELECT CASE WHEN COUNT(*) > 0 THEN 1 ELSE 0 END
        INTO v_exists
        FROM users
        WHERE email = p_email;

        RETURN v_exists;
    END check_if_user_exists;
    
    FUNCTION get_user_by_id (p_id IN NUMBER) RETURN SYS_REFCURSOR
    IS
        result_cursor SYS_REFCURSOR;
    BEGIN
        OPEN result_cursor FOR
            SELECT id, first_name, last_name, email, profile_picture_url, role
            FROM users
            WHERE id = p_id;

        RETURN result_cursor;
    END get_user_by_id;

    PROCEDURE reject_campaign (p_campaign_id IN NUMBER)
    IS
    
    BEGIN
        DELETE FROM campaigns WHERE id = p_campaign_id;
    END reject_campaign;

    FUNCTION get_successful_campaigns (p_start_date DATE, p_end_date DATE)
RETURN SYS_REFCURSOR
IS
    result_cursor SYS_REFCURSOR;
BEGIN
    OPEN result_cursor FOR
        SELECT
            c.id AS campaign_id,
            c.title AS campaign_name,
            u.first_name || ' ' || u.last_name AS organizer_name,
            (
                SELECT u2.first_name || ' ' || u2.last_name
                FROM donations d2
                JOIN users u2 ON d2.user_id = u2.id
                WHERE d2.campaign_id = c.id
                  AND d2.amount = (
                      SELECT MAX(d3.amount)
                      FROM donations d3
                      WHERE d3.campaign_id = c.id
                  )
                FETCH FIRST 1 ROWS ONLY
            ) AS top_donor_name,
            COALESCE(SUM(d.amount), 0) AS total_raised,
            c.end_date,
            cat.name AS category_name,
            COALESCE(ROUND(AVG(d.amount), 2), 0) AS average_donation
        FROM campaigns c
        JOIN users u ON c.organizer_id = u.id
        JOIN categories cat ON c.category_id = cat.id
        LEFT JOIN donations d ON c.id = d.campaign_id
        WHERE c.end_date BETWEEN p_start_date AND p_end_date
          AND c.current_money_amount >= c.target_money_amount
        GROUP BY c.id, c.title, u.first_name, u.last_name, c.end_date, cat.name;

    RETURN result_cursor;
END;

    FUNCTION get_verified_user_campaigns RETURN SYS_REFCURSOR
    IS
        result_cursor SYS_REFCURSOR;
    BEGIN
        OPEN result_cursor FOR
            SELECT
                c.id AS campaign_id,
                c.title AS campaign_name,
                u.first_name || ' ' || u.last_name AS organizer_name,
                COUNT(DISTINCT d.user_id) AS supporter_count,
                MAX(d.amount) AS highest_donation,
                cat.name AS category_name,
                c.status
            FROM campaigns c
            JOIN users u ON c.organizer_id = u.id
            JOIN categories cat ON c.category_id = cat.id
            LEFT JOIN donations d ON c.id = d.campaign_id
            WHERE u.document_photo IS NOT NULL
            GROUP BY c.id, c.title, u.first_name, u.last_name, cat.name, c.status;
    
        RETURN result_cursor;
    END;

END Crowdfunding_pkg;
/
