USE surplus_food_db;

-- 1. Insert Vendors
INSERT INTO vendors (vendor_name, business_type, contact_phone, email, address) VALUES
('Fresh Bakery', 'Bakery', '01711000001', 'contact@freshbakery.com', '123 Bread St'),
('Green Grocers', 'Supermarket', '01711000002', 'info@greengrocers.com', '456 Veggie Ave'),
('Spicy Deli', 'Restaurant', '01711000003', 'hello@spicydeli.com', '789 Spice Rd');

-- 2. Insert Receivers
INSERT INTO receivers (org_name, org_type, contact_no, daily_quota_limit) VALUES
('City Food Bank', 'NGO', '01811000001', 500),
('Hope Shelter', 'Shelter', '01811000002', 200),
('Community Kitchen', 'Community Kitchen', '01811000003', 150);

-- 3. Insert Food Batches
-- 1 fresh, 1 discounted, 1 near-expiry donation, 1 expired
INSERT INTO food_batches (vendor_id, item_name, quantity, original_price, expiry_time, batch_status) VALUES
(1, 'Sourdough Bread', 20, 50.00, DATE_ADD(NOW(), INTERVAL 18 HOUR), 'Available'),
(2, 'Fresh Produce Pack', 15, 120.00, DATE_ADD(NOW(), INTERVAL 2 HOUR), 'Discounted'),
(3, 'Lunch Meal Boxes', 10, 85.00, DATE_ADD(NOW(), INTERVAL 45 MINUTE), 'Free_Donation'),
(1, 'Assorted Pastries', 8, 40.00, DATE_SUB(NOW(), INTERVAL 2 HOUR), 'Expired');

-- 4. Insert Claims
INSERT INTO claims (batch_id, receiver_id, claimed_quantity, total_price, claim_status) VALUES
(2, 1, 5, 300.00, 'Reserved'),
(3, 2, 10, 0.00, 'Completed');
