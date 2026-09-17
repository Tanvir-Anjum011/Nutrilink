# Relational Schema Mapping

This document translates the 4 Chen ERD entities (vendors, food_batches, receivers, claims) into relational schemas.

## 1. Vendors
* **Table Name:** `vendors`
* **Description:** Stores information about the restaurants or grocery stores providing surplus food.
* **Columns:**
  * `vendor_id` (INT) - **Primary Key**
  * `name` (VARCHAR(255))
  * `address` (VARCHAR(500))
  * `contact_phone` (VARCHAR(20))

## 2. Receivers
* **Table Name:** `receivers`
* **Description:** Stores information about the NGOs or individuals receiving the food.
* **Columns:**
  * `receiver_id` (INT) - **Primary Key**
  * `name` (VARCHAR(255))
  * `ngo_registration_number` (VARCHAR(100))
  * `contact_email` (VARCHAR(255))

## 3. Food Batches
* **Table Name:** `food_batches`
* **Description:** Stores details of the surplus food batches listed by vendors.
* **Columns:**
  * `batch_id` (INT) - **Primary Key**
  * `vendor_id` (INT) - **Foreign Key** referencing `vendors(vendor_id)`
  * `item_name` (VARCHAR(255))
  * `portions` (INT) - **CHECK** (`portions >= 0`)
  * `original_price` (DECIMAL(10, 2)) - **CHECK** (`original_price >= 0`)
  * `expiry_time` (DATETIME)

## 4. Claims
* **Table Name:** `claims`
* **Description:** Records the claims made by receivers for specific food batches.
* **Columns:**
  * `claim_id` (INT) - **Primary Key**
  * `batch_id` (INT) - **Foreign Key** referencing `food_batches(batch_id)`
  * `receiver_id` (INT) - **Foreign Key** referencing `receivers(receiver_id)`
  * `claimed_portions` (INT) - **CHECK** (`claimed_portions > 0`)
  * `claim_time` (DATETIME)

---

## 3rd Normal Form (3NF) Justification

Our database schema satisfies the 3rd Normal Form (3NF) because it meets the following criteria:

1.  **First Normal Form (1NF):** All tables have a primary key, and all attributes contain atomic (indivisible) values. There are no repeating groups.
2.  **Second Normal Form (2NF):** The schema is in 1NF, and all non-key attributes are fully functionally dependent on the entire primary key. In all our tables (`vendors`, `receivers`, `food_batches`, `claims`), the primary keys are single columns (`vendor_id`, `receiver_id`, `batch_id`, `claim_id`), meaning partial dependency is not possible.
3.  **Third Normal Form (3NF):** The schema is in 2NF, and there are no transitive dependencies. Every non-prime attribute depends solely on the primary key of its table, and not on any other non-prime attribute.
    *   In `vendors`, address and phone depend only on the `vendor_id`.
    *   In `receivers`, the registration number and email depend only on the `receiver_id`.
    *   In `food_batches`, the item details and foreign key (`vendor_id`) depend only on `batch_id`.
    *   In `claims`, the claim details depend only on the `claim_id`.
