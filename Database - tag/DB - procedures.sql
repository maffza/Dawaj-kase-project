CREATE OR REPLACE FUNCTION get_campaign_by_id(p_id IN NUMBER) 
RETURN SYS_REFCURSOR AS
  ref_cursor SYS_REFCURSOR;
BEGIN
  OPEN ref_cursor FOR
    SELECT * FROM campaigns WHERE id = p_id;
  RETURN ref_cursor;
END;