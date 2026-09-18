-- Create database
CREATE DATABASE IF NOT EXISTS surplus_food_db;
USE surplus_food_db;

-- 1. Vendors Table
CREATE TABLE IF NOT EXISTS vendors (
    vendor_id INT AUTO_INCREMENT PRIMARY KEY,
    vendor_name VARCHAR(255) NOT NULL,
    business_type VARCHAR(100),
    contact_phone VARCHAR(20) UNIQUE,
    email VARCHAR(255) UNIQUE,
    address TEXT
) ENGINE=InnoDB;


-- 2. Receivers Table
CREATE TABLE IF NOT EXISTS receivers (
    receiver_id INT AUTO_INCREMENT PRIMARY KEY,
    org_name VARCHAR(255) NOT NULL,
    org_type VARCHAR(100),
    contact_no VARCHAR(20) UNIQUE,
    daily_quota_limit INT CHECK (daily_quota_limit > 0)
) ENGINE=InnoDB;

-- 3. Food Batches Table
CREATE TABLE IF NOT EXISTS food_batches (
    batch_id INT AUTO_INCREMENT PRIMARY KEY,
    vendor_id INT NOT NULL,
    item_name VARCHAR(255) NOT NULL,
    quantity INT NOT NULL CHECK (quantity >= 0),
    original_price DECIMAL(10, 2) NOT NULL CHECK (original_price >= 0),
    prepared_time DATETIME DEFAULT CURRENT_TIMESTAMP,
    expiry_time DATETIME NOT NULL,
    batch_status VARCHAR(50) DEFAULT 'Available',
    FOREIGN KEY (vendor_id) REFERENCES vendors(vendor_id) ON DELETE CASCADE
) ENGINE=InnoDB;

-- 4. Claims Associative Table
CREATE TABLE IF NOT EXISTS claims (
    claim_id INT AUTO_INCREMENT PRIMARY KEY,
    batch_id INT NOT NULL,
    receiver_id INT NOT NULL,
    claimed_quantity INT NOT NULL CHECK (claimed_quantity > 0),
    total_price DECIMAL(10, 2) NOT NULL CHECK (total_price >= 0),
    claim_timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    claim_status VARCHAR(50) DEFAULT 'Reserved',
    FOREIGN KEY (batch_id) REFERENCES food_batches(batch_id) ON DELETE CASCADE,
    FOREIGN KEY (receiver_id) REFERENCES receivers(receiver_id) ON DELETE CASCADE
) ENGINE=InnoDB;
