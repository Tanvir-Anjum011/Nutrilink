# Nutrilink — Project Guidelines & Rules

**Course:** CSE 3522 (Database Management Systems Lab)
**Project:** Surplus Food Redistribution Network

---

### What This Project Is

Nutrilink connects food businesses (restaurants, bakeries, caterers across Dhaka) with local charities and shelters to cut down on edible food waste.

---

### Tech Stack & The Golden Rule

- **Frontend:** Python with Streamlit.
- **Database:** MySQL 8.0+ running the **InnoDB** engine exclusively (required for foreign key constraints and atomic transactions).
- **Database Driver:** `mysql-connector-python` (Official native driver).
- **THE BIG RULE (No ORMs):**
  Do not use SQLAlchemy, Peewee, Prisma, or any other ORM. Every interaction with MySQL must be written in **raw parameterized SQL** (`cursor.execute("SELECT ... WHERE id = %s", (val,))`). Evaluators are grading raw database engineering, not framework shortcuts.

---

### The 4 Core Tables

1. **`vendors`**: Food businesses posting surplus food (restaurants, bakeries, supermarkets).
2. **`receivers`**: Verified non-profit organizations, charities, and shelters claiming surplus items.
3. **`food_batches`**: The food listings themselves (item name, portion counts, original price, and expiration timestamp).
4. **`claims`**: The associative bridge table resolving the many-to-many relationship between receivers and food batches.

---

### Database Standards We Must Enforce

- **Clean Normalization (3NF):** Every attribute depends strictly on the primary key. No duplicated columns and zero transitive dependencies across tables.
- **Engine-Level Data Integrity:** Enforce validation rules directly inside the MySQL engine using `CHECK` constraints (e.g., `quantity >= 0`), `UNIQUE` constraints (phone and email), and `FOREIGN KEY ... ON DELETE CASCADE`. Do not rely solely on frontend Python logic.
- **ACID Transactions:** Food claims and inventory decrements must run inside explicit transaction blocks (`START TRANSACTION`, `COMMIT`, `ROLLBACK`) to guarantee that claim records and quantity deductions succeed or fail together.

---

### Master Implementation Timeline

- **Week 1 (Design & Setup):** Chen ERD diagram, relational schema mapping (`database/schema_mapping.md`), and initial Streamlit UI prototype (`app.py`). _(Complete)_
- **Week 2 (DDL Implementation):** Normalized DDL script (`database/01_schema.sql`), engine-level constraints, and boundary test records (`database/02_seed_data.sql`). _(Complete)_
- **Week 3 (Live Integration):** Connect Streamlit directly to MySQL using `mysql-connector-python`, replacing mock lists with real `SELECT` feeds and parameterized `INSERT` statements. _(Next Milestone)_
- **Week 4 (Advanced SQL):** Stored procedures for claims and quota checks, triggers for automated batch expiry handling, and analytical administrative views.
- **Week 5 (Validation & Defense):** Edge-case testing, performance verification, and final semester project defense.
