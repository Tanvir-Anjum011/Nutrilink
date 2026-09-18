# 🍲 Nutrilink — Surplus Food Redistribution Network

> A relational database management system connecting commercial food donors (restaurants, bakeries, caterers) across Dhaka with verified charities and shelters to cut down edible food waste.

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue?logo=python)](https://python.org)
[![Frontend](https://img.shields.io/badge/Frontend-Streamlit-FF4B4B?logo=streamlit)](https://streamlit.io)
[![Database](https://img.shields.io/badge/Database-MySQL%208.0%20(InnoDB)-00758F?logo=mysql)](https://mysql.com)
[![Architecture](https://img.shields.io/badge/Schema-3NF%20Normalized-green)]()
[![Integrity](https://img.shields.io/badge/Integrity-Engine--Level%20Constraints-orange)]()
[![Live Demo](https://img.shields.io/badge/Streamlit%20Cloud-Live%20Prototype-success?logo=streamlit)](https://share.streamlit.io)

---

## 📌 Project Overview

Nutrilink is a university Database Management Systems (DBMS) lab project engineered to solve commercial food wastage in urban Dhaka. It provides a transactional platform where food businesses can log surplus inventory before expiration, and verified non-profits can claim portions in real time under strict daily quota constraints.

### Core Architecture Principles
* **Raw Parameterized SQL:** Zero Object-Relational Mappings (No ORMs like SQLAlchemy or Peewee). Every query runs directly against the engine via `mysql-connector-python`.
* **Third Normal Form (3NF):** Elimination of transitive and partial dependencies across all relational tables.
* **Engine-Level Integrity:** Business constraints (`CHECK`, `UNIQUE`, `FOREIGN KEY ... ON DELETE CASCADE`) enforced directly inside the MySQL InnoDB storage engine rather than relying solely on frontend validation.
* **ACID Transaction Safeguards:** Inventory claim operations designed to run within atomic transaction blocks (`START TRANSACTION`, `COMMIT`, `ROLLBACK`) to prevent race conditions and double claims.

---

## 🗄️ Relational Schema Design

The database schema (`surplus_food_db`) consists of 4 core tables running exclusively on the **InnoDB** storage engine:

| Table | Entity Type | Primary Key | Key Relationships & Constraints |
| :--- | :--- | :--- | :--- |
| **`vendors`** | Strong Entity | `vendor_id` | Unique `contact_phone` and `email` constraints; donor business profiles across Dhaka. |
| **`receivers`** | Strong Entity | `receiver_id` | Unique `contact_no`; enforced `daily_quota_limit > 0`. |
| **`food_batches`** | Dependent Entity | `batch_id` | Foreign Key to `vendors(vendor_id)` (`ON DELETE CASCADE`); check constraints (`quantity >= 0`, `original_price >= 0`). |
| **`claims`** | Associative Entity | `claim_id` | Resolves $M:N$ relationship between `receivers` and `food_batches`; check constraints (`claimed_quantity > 0`, `total_price >= 0`). |

---

## 📂 Project Structure

```text
Nutrilink/
├── .gitignore                  # Excludes venv, OS metadata, and environment caches
├── README.md                   # Project documentation and setup guide
├── requirements.txt            # Minimal runtime Python dependencies
├── app.py                      # Streamlit web application frontend
├── project_Rules.md            # Course-mandated architectural and SQL guidelines
└── database/
    ├── 01_schema.sql           # DDL: Database creation, table definitions, constraints
    ├── 02_seed_data.sql        # DML: Realistic boundary seed records for Dhaka zone
    ├── Test.sql                # Verification queries and referential integrity tests
    └── schema_mapping.md       # Relational mapping documentation from Chen ERD
