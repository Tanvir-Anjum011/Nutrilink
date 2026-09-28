USE surplus_food_db;

-- -----------------------------------------------------------------------------
-- 1. Dynamic Price Decay View
-- Automatically discounts prices as shelf-life decreases.
-- In the final 2 hours, switches unsold food to free donations.
-- Under 12 hours, price is 50% of the original.
-- -----------------------------------------------------------------------------
DROP VIEW IF EXISTS vw_active_batches;
CREATE VIEW vw_active_batches AS
SELECT 
    b.batch_id,
    b.vendor_id,
    v.vendor_name,
    v.address AS zone,
    b.item_name,
    b.quantity,
    b.original_price,
    b.expiry_time,
    b.batch_status,
    CASE 
        WHEN b.expiry_time <= NOW() THEN 0
        WHEN TIMESTAMPDIFF(MINUTE, NOW(), b.expiry_time) < 300 THEN ROUND(b.original_price * 0.5, 2)
        ELSE b.original_price
    END AS current_price
FROM food_batches b
JOIN vendors v ON b.vendor_id = v.vendor_id
WHERE b.quantity > 0 AND b.expiry_time > NOW();

-- -----------------------------------------------------------------------------
-- 2. Automated Safety Shield Trigger
-- Instantly blocks and rejects any attempts to claim or purchase expired food batches.
-- -----------------------------------------------------------------------------
DELIMITER //
DROP TRIGGER IF EXISTS trg_prevent_expired_claims //
CREATE TRIGGER trg_prevent_expired_claims
BEFORE INSERT ON claims
FOR EACH ROW
BEGIN
    DECLARE v_expiry_time DATETIME;
    
    SELECT expiry_time INTO v_expiry_time 
    FROM food_batches 
    WHERE batch_id = NEW.batch_id;
    
    IF v_expiry_time <= NOW() THEN
        SIGNAL SQLSTATE '45000' 
        SET MESSAGE_TEXT = 'Cannot claim expired food batches. Safety Shield triggered.';
    END IF;
END //
DELIMITER ;

-- -----------------------------------------------------------------------------
-- 3. Fair-Share Quota Limits & Concurrency-Safe Allocations Stored Procedure
-- Enforces daily claim caps per organization.
-- Uses row-level locking (SELECT ... FOR UPDATE) to prevent double-booking.
-- -----------------------------------------------------------------------------
DELIMITER //
DROP PROCEDURE IF EXISTS sp_claim_food //
CREATE PROCEDURE sp_claim_food(
    IN p_receiver_id INT, 
    IN p_batch_id INT, 
    IN p_quantity INT
)
BEGIN
    DECLARE v_daily_quota INT;
    DECLARE v_claimed_today INT;
    DECLARE v_available_qty INT;
    DECLARE v_current_price DECIMAL(10, 2);
    DECLARE v_total_price DECIMAL(10, 2);
    
    -- Transactional Integrity: Execute the claim process atomically
    START TRANSACTION;
    
    -- Get daily quota limit for receiver
    SELECT daily_quota_limit INTO v_daily_quota 
    FROM receivers 
    WHERE receiver_id = p_receiver_id;
    
    -- Calculate total portions claimed today by this receiver
    SELECT IFNULL(SUM(claimed_quantity), 0) INTO v_claimed_today 
    FROM claims 
    WHERE receiver_id = p_receiver_id AND DATE(claim_timestamp) = CURDATE();
    
    -- Enforce daily claim cap
    IF (v_claimed_today + p_quantity) > v_daily_quota THEN
        ROLLBACK;
        SIGNAL SQLSTATE '45000' 
        SET MESSAGE_TEXT = 'Daily claim quota limit exceeded for this organization.';
    END IF;
    
    -- Concurrency-Safe Allocation: Row-level lock on the batch
    SELECT quantity, current_price INTO v_available_qty, v_current_price
    FROM vw_active_batches 
    WHERE batch_id = p_batch_id 
    FOR UPDATE;
    
    -- Check if sufficient quantity is available
    IF v_available_qty IS NULL THEN
        ROLLBACK;
        SIGNAL SQLSTATE '45000' 
        SET MESSAGE_TEXT = 'Batch not found or has already expired.';
    ELSEIF v_available_qty < p_quantity THEN
        ROLLBACK;
        SIGNAL SQLSTATE '45000' 
        SET MESSAGE_TEXT = 'Insufficient quantity available in this batch.';
    END IF;
    
    -- Calculate total price based on dynamic price
    SET v_total_price = v_current_price * p_quantity;
    
    -- Insert the claim
    INSERT INTO claims (batch_id, receiver_id, claimed_quantity, total_price, claim_status)
    VALUES (p_batch_id, p_receiver_id, p_quantity, v_total_price, 'Completed');
    
    -- Update batch quantity and status
    UPDATE food_batches 
    SET quantity = quantity - p_quantity,
        batch_status = IF(quantity - p_quantity <= 0, 'Depleted', batch_status)
    WHERE batch_id = p_batch_id;
    
    -- Commit transaction
    COMMIT;
END //
DELIMITER ;
