INSERT INTO categories (name, description)
VALUES ('Technology', 'Campaigns related to technology and innovation');
INSERT INTO categories (name, description)
VALUES ('Health', 'Campaigns supporting health and wellness initiatives');
INSERT INTO categories (name, description)
VALUES ('Education', 'Campaigns for educational purposes');
INSERT INTO categories (name, description)
VALUES ('Environment', 'Campaigns aimed at protecting the environment and promoting sustainability');
INSERT INTO categories (name, description)
VALUES ('Animals', 'Campaigns supporting animal welfare, shelters, and wildlife protection');
INSERT INTO categories (name, description)
VALUES ('Community', 'Campaigns to support local community projects and social initiatives');

INSERT INTO users (first_name, last_name, address, city, email, password_hash, role) 
VALUES ('John', 'Doe', '123 Maple Street', 'Springfield', 'john.doe@example.com', 'ha665a45920422f9d417e4867efdc4fb8a04a1f3fff1fa07e998e86f7f7a27ae3', 'Organizer');
INSERT INTO users (first_name, last_name, address, city, email, password_hash, role) 
VALUES ('Erwin', 'Schulz', '135 Antoniusstraße', 'Magdeburg', 'erwin.schulz@example.com', 'ha665a45920422f9d417e4867efdc4fb8a04a1f3fff1fa07e998e86f7f7a27ae3', 'Organizer');
INSERT INTO users (first_name, last_name, address, city, email, password_hash, role) 
VALUES ('Jane', 'Smith', '456 Oak Avenue', 'Springfield', 'jane.smith@example.com', 'a665a45920422f9d417e4867efdc4fb8a04a1f3fff1fa07e998e86f7f7a27ae3', 'Supporter');
INSERT INTO users (first_name, last_name, address, city, email, password_hash, role) 
VALUES ('Alice', 'Johnson', '789 Pine Road', 'Metropolis', 'alice.johnson@example.com', 'a665a45920422f9d417e4867efdc4fb8a04a1f3fff1fa07e998e86f7f7a27ae3', 'Supporter');

INSERT INTO campaigns (title, description, short_description, target_money_amount, current_money_amount, start_date, end_date, status, image_url, organizer_id, category_id) 
VALUES ('Tech for All', 'A campaign to provide tech resources to underprivileged students', 'Providing laptops to schools', 10000, 2500, SYSDATE, SYSDATE + 30, 'Active', '', 1, 1);
INSERT INTO campaigns (title, description, short_description, target_money_amount, current_money_amount, start_date, end_date, status, image_url, organizer_id, category_id) 
VALUES ('Health First', 'Supporting mental health awareness', 'Mental health workshops', 5000, 1200, SYSDATE, SYSDATE + 15, 'Active', '', 2, 2);
INSERT INTO campaigns (title, description, short_description, target_money_amount, current_money_amount, start_date, end_date, status, image_url, organizer_id, category_id) 
VALUES ('Clean Oceans Project', 'An initiative to remove plastic waste from oceans and promote recycling', 'Save the oceans from plastic', 20000, 3500, SYSDATE, SYSDATE + 60, 'Active', '', 1, 4);
INSERT INTO campaigns (title, description, short_description, target_money_amount, current_money_amount, start_date, end_date, status, image_url, organizer_id, category_id) 
VALUES ('Animal Shelter Renovation', 'Renovating the local animal shelter to improve living conditions for rescued animals', 'Better homes for rescued animals', 8000, 1500, SYSDATE, SYSDATE + 45, 'Active', '', 1, 5);
INSERT INTO campaigns (title, description, short_description, target_money_amount, current_money_amount, start_date, end_date, status, image_url, organizer_id, category_id) 
VALUES ('Library for Everyone', 'Creating a public library in a rural community to promote literacy', 'Books for all ages', 12000, 4000, SYSDATE, SYSDATE + 90, 'Active', '', 2, 3);

INSERT INTO donations (amount, message, campaign_id, user_id) 
VALUES (100, 'Great initiative!', 1, 3);
INSERT INTO donations (amount, message, campaign_id, user_id) 
VALUES (5, 'Gocha gocha 5 zlotych', 1, 4);
INSERT INTO donations (amount, message, campaign_id, user_id) 
VALUES (50, 'Keep up the good work!', 2, 3);
INSERT INTO donations (amount, message, campaign_id, user_id) 
VALUES (20, 'Happy to support this cause!', 3, 4);
INSERT INTO donations (amount, message, campaign_id, user_id) 
VALUES (15, 'Every bit helps!', 2, 3);

INSERT INTO comments (comment_text, campaign_id, user_id) 
VALUES ('This is an amazing campaign!', 1, 3);
INSERT INTO comments (comment_text, campaign_id, user_id) 
VALUES ('Happy to support!', 3, 4);

INSERT INTO rewards (description, amount_required, campaign_id) 
VALUES ('Thank you card', 20, 1);
INSERT INTO rewards (description, amount_required, campaign_id) 
VALUES ('T-shirt', 50, 1);
INSERT INTO rewards (description, amount_required, campaign_id) 
VALUES ('Book', 100, 1);

INSERT INTO favourites (user_id, campaign_id) 
VALUES (3, 1);
INSERT INTO favourites (user_id, campaign_id) 
VALUES (4, 2);
