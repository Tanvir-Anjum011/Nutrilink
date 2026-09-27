# Nutrilink: Surplus Food Redistribution Network

![Python](https://img.shields.io/badge/Python-3.9%2B-blue?logo=python&logoColor=white)
![MySQL](https://img.shields.io/badge/MySQL-InnoDB-4479A1?logo=mysql&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-App-FF4B4B?logo=streamlit&logoColor=white)
![Normalization](https://img.shields.io/badge/Architecture-3NF-success)

Nutrilink is a relational database management system engineered to connect commercial food donors (restaurants, bakeries, caterers) across Dhaka with verified charities and shelters to eliminate edible food waste. The platform is built using **Python**, **Streamlit**, and **MySQL (InnoDB)**, leveraging raw parameterized SQL execution without Object-Relational Mappers (ORMs).

---

## Database Architecture (`surplus_food_db`)

The relational schema is structured in **Third Normal Form (3NF)** across four core tables operating on `ENGINE=InnoDB`:

| Table | Entity Type | Primary Key | Keys & Constraints | Description |
| :--- | :--- | :--- | :--- | :--- |
| **`vendors`** | Strong Entity | `vendor_id` | `UNIQUE(contact_phone, email)` | Commercial food donors and local businesses. |
| **`receivers`** | Strong Entity | `receiver_id` | `UNIQUE(contact_no)`<br>`CHECK(daily_quota_limit > 0)` | Verified non-profit shelters, NGOs, and food banks. |
| **`food_batches`** | Entity | `batch_id` | `FK(vendor_id) REFERENCES vendors(vendor_id) ON DELETE CASCADE`<br>`CHECK(quantity >= 0)`<br>`CHECK(original_price >= 0)` | Surplus food inventory listings with expiration timestamps. |
| **`claims`** | Associative | `claim_id` | `FK(batch_id) REFERENCES food_batches`<br>`FK(receiver_id) REFERENCES receivers`<br>`CHECK(claimed_quantity > 0)`<br>`CHECK(total_price >= 0)` | Resolves Many-to-Many ($M:N$) claim transactions between receivers and food batches. |

---

## Core Engineering Rules

* **Direct SQL Execution:** No ORMs (such as SQLAlchemy or Peewee). All database interactions execute strictly via raw parameterized queries (`cursor.execute`) using `mysql-connector-python` to prevent SQL injection.
* **Engine-Level Validation:** Domain bounds, data integrity, and referential actions are strictly enforced at the database level by the MySQL InnoDB engine using `CHECK` constraints and `ON DELETE CASCADE`.
* **ACID Transactions:** Claim allocations utilize atomic transaction blocks (`START TRANSACTION`, `COMMIT`, `ROLLBACK`) to guarantee transaction isolation, eliminate race conditions, and prevent inventory double-claims.

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
