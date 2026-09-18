USE surplus_food_db;

SELECT 
    v.vendor_name,
    v.business_type,
    b.item_name,
    b.quantity,
    b.original_price,
    b.expiry_time,
    b.batch_status
FROM food_batches b
INNER JOIN vendors v ON b.vendor_id = v.vendor_id
ORDER BY b.expiry_time ASC;
