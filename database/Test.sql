-- USE surplus_food_db;

-- SELECT 
--     v.vendor_name,
--     v.business_type,
--     b.item_name,
--     b.quantity,
--     b.original_price,
--     b.expiry_time,
--     b.batch_status
-- FROM food_batches b
-- INNER JOIN vendors v ON b.vendor_id = v.vendor_id
-- ORDER BY b.expiry_time ASC;

-- SELECT 
--     v.vendor_name, 
--     COUNT(f.batch_id) AS total_batches,
--     SUM(f.quantity) AS total_food_items
-- FROM vendors v
-- LEFT JOIN food_batches f ON v.vendor_id = f.vendor_id
-- GROUP BY v.vendor_name
-- ORDER BY total_food_items DESC;

