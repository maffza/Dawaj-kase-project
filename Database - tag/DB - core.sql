DROP TABLE users CASCADE CONSTRAINTS;
/
DROP SEQUENCE users_seq;
/
BEGIN
    EXECUTE IMMEDIATE 'CREATE SEQUENCE users_seq
                        START WITH 1
                        INCREMENT BY 1
                        NOCACHE
                        NOCYCLE';
EXCEPTION
    WHEN OTHERS THEN
        NULL;
END;
/
CREATE TABLE users (
    id                  NUMBER PRIMARY KEY,
    first_name          VARCHAR2(30) NOT NULL,
    last_name           VARCHAR2(30) NOT NULL,
    address             VARCHAR2(100),
    city                VARCHAR2(40),
    email               VARCHAR2(80) NOT NULL UNIQUE,
    phone               NUMBER,
    bank_account        NUMBER,
    document_photo      VARCHAR2(500),
    password_hash       VARCHAR2(255) NOT NULL,
    profile_picture_url VARCHAR2(500),
    role                VARCHAR2(30) DEFAULT 'Supporter',
    description         CLOB,
    creation_date       DATE,
    modify_date         DATE
);
/
CREATE OR REPLACE TRIGGER users_add BEFORE
    INSERT ON users
    FOR EACH ROW
BEGIN
    :new.ID := users_seq.NEXTVAL;
    :new.creation_date := sysdate;
END;
/
CREATE OR REPLACE TRIGGER users_update BEFORE
    UPDATE ON users
    FOR EACH ROW
BEGIN
    :new.modify_date := sysdate;
END;
/
DROP TABLE campaigns CASCADE CONSTRAINTS;
/
DROP SEQUENCE campaigns_seq;
/
BEGIN
    EXECUTE IMMEDIATE 'CREATE SEQUENCE campaigns_seq
                        START WITH 1
                        INCREMENT BY 1
                        NOCACHE
                        NOCYCLE';
EXCEPTION
    WHEN OTHERS THEN
        NULL;
END;
/
CREATE TABLE campaigns (
    id                   NUMBER PRIMARY KEY,
    title                VARCHAR2(50),
    description          CLOB,
    short_description    VARCHAR(500), -- UPDATE 23.11.2024
    target_money_amount  NUMBER,
    current_money_amount NUMBER,
    start_date           DATE,
    end_date             DATE,
    status               VARCHAR2(30),
    image_url            VARCHAR2(500),
    organizer_id         NUMBER,
    category_id          NUMBER,
    creation_date        DATE,
    modify_date          DATE
);
/
ALTER TABLE campaigns
    ADD CONSTRAINT fk_userscampaigns FOREIGN KEY ( organizer_id )
        REFERENCES users ( id );
/
ALTER TABLE campaigns
    ADD CONSTRAINT fk_userscategories FOREIGN KEY ( category_id )
        REFERENCES categories ( id );
/
CREATE OR REPLACE TRIGGER campaigns_add BEFORE
    INSERT ON campaigns
    FOR EACH ROW
BEGIN
    :new.ID := campaigns_seq.NEXTVAL;
    :new.creation_date := sysdate;
END;
/
CREATE OR REPLACE TRIGGER campaigns_update BEFORE
    UPDATE ON campaigns
    FOR EACH ROW
BEGIN
    :new.modify_date := sysdate;
END;
/
DROP TABLE donations CASCADE CONSTRAINTS;
/
DROP SEQUENCE donations_seq;
/
BEGIN
    EXECUTE IMMEDIATE 'CREATE SEQUENCE donations_seq
                        START WITH 1
                        INCREMENT BY 1
                        NOCACHE
                        NOCYCLE';
EXCEPTION
    WHEN OTHERS THEN
        NULL;
END;
/
CREATE TABLE donations (
    id            NUMBER PRIMARY KEY,
    amount        NUMBER NOT NULL,
    message       CLOB,
    campaign_id   NUMBER,
    user_id       NUMBER,
    creation_date DATE,
    modify_date   DATE
);
/
ALTER TABLE donations
    ADD CONSTRAINT fk_donationscampaigns FOREIGN KEY ( campaign_id )
        REFERENCES campaigns ( id );
/
ALTER TABLE donations
    ADD CONSTRAINT fk_donationsusers FOREIGN KEY ( user_id )
        REFERENCES users ( id );
/
CREATE OR REPLACE TRIGGER donations_add BEFORE
    INSERT ON donations
    FOR EACH ROW
BEGIN
    :new.ID := donations_seq.NEXTVAL;
    :new.creation_date := sysdate;
END;
/
CREATE OR REPLACE TRIGGER donations_update BEFORE
    UPDATE ON donations
    FOR EACH ROW
BEGIN
    :new.modify_date := sysdate;
END;
/
DROP TABLE comments CASCADE CONSTRAINTS;
/
DROP SEQUENCE comments_seq;
/
BEGIN
    EXECUTE IMMEDIATE 'CREATE SEQUENCE comments_seq
                        START WITH 1
                        INCREMENT BY 1
                        NOCACHE
                        NOCYCLE';
EXCEPTION
    WHEN OTHERS THEN
        NULL;
END;
/
CREATE TABLE comments (
    id            NUMBER PRIMARY KEY,
    comment_text  CLOB NOT NULL,
    campaign_id   NUMBER,
    user_id       NUMBER,
    creation_date DATE,
    modify_date   DATE
);
/
ALTER TABLE comments
    ADD CONSTRAINT fk_commentscampaigns FOREIGN KEY ( campaign_id )
        REFERENCES campaigns ( id );
/
ALTER TABLE comments
    ADD CONSTRAINT fk_commentsusers FOREIGN KEY ( user_id )
        REFERENCES users ( id );
/
CREATE OR REPLACE TRIGGER comments_add BEFORE
    INSERT ON comments
    FOR EACH ROW
BEGIN
    :new.ID := comments_seq.NEXTVAL;
    :new.creation_date := sysdate;
END;
/
CREATE OR REPLACE TRIGGER comments_update BEFORE
    UPDATE ON comments
    FOR EACH ROW
BEGIN
    :new.modify_date := sysdate;
END;
/
DROP TABLE rewards CASCADE CONSTRAINTS;
/
DROP SEQUENCE rewards_seq;
/
BEGIN
    EXECUTE IMMEDIATE 'CREATE SEQUENCE rewards_seq
                        START WITH 1
                        INCREMENT BY 1
                        NOCACHE
                        NOCYCLE';
EXCEPTION
    WHEN OTHERS THEN
        NULL;
END;
/
CREATE TABLE rewards (
    id              NUMBER PRIMARY KEY,
    description     CLOB NOT NULL,
    amount_required NUMBER NOT NULL,
    campaign_id     NUMBER,
    creation_date   DATE,
    modify_date     DATE
);
/
ALTER TABLE rewards
    ADD CONSTRAINT fk_rewardscampaigns FOREIGN KEY ( campaign_id )
        REFERENCES campaigns ( id );
/
CREATE OR REPLACE TRIGGER rewards_add BEFORE
    INSERT ON rewards
    FOR EACH ROW
BEGIN
    :new.ID := rewards_seq.NEXTVAL;
    :new.creation_date := sysdate;
END;
/
CREATE OR REPLACE TRIGGER rewards_update BEFORE
    UPDATE ON rewards
    FOR EACH ROW
BEGIN
    :new.modify_date := sysdate;
END;
/
DROP TABLE categories CASCADE CONSTRAINTS;
/
DROP SEQUENCE categories_seq;
/
BEGIN
    EXECUTE IMMEDIATE 'CREATE SEQUENCE categories_seq
                        START WITH 1
                        INCREMENT BY 1
                        NOCACHE
                        NOCYCLE';
EXCEPTION
    WHEN OTHERS THEN
        NULL;
END;
/
CREATE TABLE categories (
    id            NUMBER PRIMARY KEY,
    name          VARCHAR2(40) NOT NULL,
    description   VARCHAR2(255),
    creation_date DATE,
    modify_date   DATE
);
/
CREATE OR REPLACE TRIGGER categories_add BEFORE
    INSERT ON categories
    FOR EACH ROW
BEGIN
    :new.ID := categories_seq.NEXTVAL;
    :new.creation_date := sysdate;
END;
/
CREATE OR REPLACE TRIGGER categories_update BEFORE
    UPDATE ON categories
    FOR EACH ROW
BEGIN
    :new.modify_date := sysdate;
END;
/
DROP TABLE favourites CASCADE CONSTRAINTS;
/
DROP SEQUENCE favourites_seq;
/
BEGIN
    EXECUTE IMMEDIATE 'CREATE SEQUENCE favourites_seq
                        START WITH 1
                        INCREMENT BY 1
                        NOCACHE
                        NOCYCLE';
EXCEPTION
    WHEN OTHERS THEN
        NULL;
END;
/
-- UPDATE 24.11.2024
CREATE TABLE favourites (
    id            NUMBER PRIMARY KEY,
    user_id       NUMBER,
    campaign_id   NUMBER,
    creation_date DATE,
    modify_date   DATE
);
/
ALTER TABLE favourites
    ADD CONSTRAINT fk_favouritesusers FOREIGN KEY ( user_id )
        REFERENCES users ( id );
/
ALTER TABLE favourites
    ADD CONSTRAINT fk_favouritescampaigns FOREIGN KEY ( campaign_id )
        REFERENCES campaigns ( id );
/
CREATE OR REPLACE TRIGGER favourites_add BEFORE
    INSERT ON favourites
    FOR EACH ROW
BEGIN
    :new.ID := favourites_seq.NEXTVAL;
    :new.creation_date := sysdate;
END;
/
CREATE OR REPLACE TRIGGER favourites_update BEFORE
    UPDATE ON favourites
    FOR EACH ROW
BEGIN
    :new.modify_date := sysdate;
END;
/