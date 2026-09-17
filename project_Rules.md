# Nutrilink

**Course:** CSE 3522 - Database Management Systems Lab

---

## 1. Technical Stack Constraints

- **Database Engine:** MySQL 8.0+ (InnoDB engine exclusively).
- **Database Driver:** `mysql-connector-python` (Official native driver).
- **Frontend / Application:** Python 3 + Streamlit.
- **Strict Rule on ORMs:** NEVER suggest, write, or import ORMs (No SQLAlchemy, Prisma, Peewee, Tortoise, etc.). All database interactions must use direct parameterized SQL (`cursor.execute(...)`).

---

## 2. Core Relational Entities

- **Vendors:** Stores food business donors (restaurants, bakeries, supermarkets).
- **Receivers:** Stores verified non-profit organizations, food banks, and shelters.
- **Food Batches:** Tracks surplus food inventory, quantity, pricing, and expiration timestamps.
- **Claims:** Associative transaction entity resolving the Many-to-Many relationship between receivers and food batches.

---

## 3. Database Engineering Principles

- **Third Normal Form (3NF):** Atomic attributes, fully functional dependencies on primary keys, zero transitive dependencies.
- **Engine-Level Integrity:** Enforce data safety at the storage layer via `CHECK` constraints, `UNIQUE` keys, and `FOREIGN KEY ... ON DELETE CASCADE`.
- **ACID Transactions:** All claims and inventory decrements must use explicit `START TRANSACTION`, `COMMIT`, and `ROLLBACK` blocks.

---

## 4. Master 5-Week Implementation Roadmap

- **Week 1: Interface & Database Design:**
  - Build Streamlit UI prototype.
  - Map Chen ERD to physical relations (`database/schema_mapping.md`).
  - Verify local MySQL environment connections.
- **Week 2: DDL Implementation:**
  - Implement normalized DDL schema (`database/01_schema.sql`).
  - Populate realistic boundary seed records (`database/02_seed_data.sql`).
  - Verify table structures, constraints, and foreign key cascades.
- **Week 3: DML Operations & Live Integration:**
  - Connect Streamlit directly to MySQL using `mysql-connector-python`.
  - Replace session state mocks with live parameterized queries.
  - Implement transactional claims logic.
- **Week 4: Advanced Database Features:**
  - Implement stored procedures for claiming and quota checks.
  - Add automatic batch status triggers.
  - Create administrative analytical views and performance indexes.
- **Week 5: Final Validation & Defense:**
  - End-to-end stress testing.
  - Presentation rehearsal and code delivery.

---

## 5. Active Sprint

- **Status:** Week 1 and Week 2 fully completed and verified.
- **Current Focus:** Presentation defense prep and Week 3 DML integration.
