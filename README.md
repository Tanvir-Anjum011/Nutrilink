# Nutrilink — Surplus Food Redistribution Network

Nutrilink is a relational database management system designed to connect commercial food donors (restaurants, bakeries, caterers) across Dhaka with verified charities and shelters to eliminate edible food waste. The platform runs on Python, Streamlit, and MySQL 8.0 (InnoDB) using raw parameterized SQL without ORMs.

---

## Database Architecture (`surplus_food_db`)

The relational schema is structured in Third Normal Form (3NF) across 4 core tables running on `ENGINE=InnoDB`:

| Table | Entity Type | Primary Key | Keys & Constraints | Description |
| :--- | :--- | :--- | :--- | :--- |
| **`vendors`** | Strong Entity | `vendor_id` | `UNIQUE(contact_phone, email)` | Commercial food donors and local businesses. |
| **`receivers`** | Strong Entity | `receiver_id` | `UNIQUE(contact_no)`, `CHECK(daily_quota_limit > 0)` | Verified non-profit shelters, NGOs, and food banks. |
| **`food_batches`** | Entity | `batch_id` | `FK(vendor_id) REFERENCES vendors(vendor_id) ON DELETE CASCADE`, `CHECK(quantity >= 0)`, `CHECK(original_price >= 0)` | Surplus food inventory listings with expiration timestamps. |
| **`claims`** | Associative | `claim_id` | `FK(batch_id) REFERENCES food_batches`, `FK(receiver_id) REFERENCES receivers`, `CHECK(claimed_quantity > 0)`, `CHECK(total_price >= 0)` | Resolves Many-to-Many ($M:N$) claim transactions between receivers and food batches. |

---

## Core Engineering Rules

* **Direct SQL Execution:** No ORMs (such as SQLAlchemy or Peewee). All database interactions execute via raw parameterized queries (`cursor.execute`) using `mysql-connector-python`.
* **Engine-Level Validation:** Domain bounds and referential actions are enforced by the MySQL InnoDB engine using `CHECK` constraints and `ON DELETE CASCADE`.
* **ACID Transactions:** Claim allocations use atomic transaction blocks (`START TRANSACTION`, `COMMIT`, `ROLLBACK`) to prevent race conditions and double-claims.

---

## Repository Structure

```text
Nutrilink/
├── app.py                  # Streamlit web application frontend
├── requirements.txt        # Python package dependencies
├── project_Rules.md        # Architectural guidelines and SQL standards
├── .gitignore              # Environment and cache exclusion rules
├── README.md               # Project documentation
└── database/
    ├── 01_schema.sql       # DDL: Database creation, table definitions, constraints
    ├── 02_seed_data.sql    # DML: Realistic boundary seed records
    ├── Test.sql            # Verification queries and relational JOIN tests
    └── schema_mapping.md   # Relational mapping documentation from Chen ERD
