# Nutrilink ~ Project Rules & Guidelines

**Project:** Surplus Food Redistribution Network
**Course:** CSE 3522

### What We Are Building

Nutrilink connects local restaurants, bakeries, and caterers across Dhaka with shelters and charities to reduce daily food waste.

---

### Non-Negotiable Rules

- **No ORMs Allowed:** Do NOT use SQLAlchemy, Peewee, or Django ORM. Sir clearly stated we must write raw SQL. All queries must be executed directly using `cursor.execute()` and `mysql-connector-python`.
- **InnoDB Engine Only:** Make sure every table uses `ENGINE=InnoDB`. If we use MyISAM, foreign keys and rollback won't work, and we will lose marks.
- **Database Checks Over Python Checks:** Don't just validate numbers in Streamlit. Put `CHECK` constraints right into the table definitions (e.g., `quantity >= 0`, `daily_quota_limit > 0`) so bad data gets rejected by MySQL itself.
- **Always Parameterize Queries:** Never use Python f-strings or string concatenation for SQL queries (e.g., don't do `f"SELECT * FROM users WHERE id = {user_id}"`). Always use `%s` placeholders to prevent syntax bugs and SQL injection.
- **Safe Claims (Transactions):** When a charity claims food, updating the batch count and creating the claim must be wrapped in a transaction (`START TRANSACTION`, `COMMIT`, `ROLLBACK`).

---

### The 4 Tables We Use

1. **`vendors`**: Restaurants and food shops donating surplus food.
2. **`receivers`**: Verified charities, shelters, and NGOs claiming items.
3. **`food_batches`**: The actual food items, portions, prices, and expiry times.
4. **`claims`**: The bridge table tracking which NGO claimed which batch, how much, and when.

---

### Git & Collaboration Rules

- **Always pull first:** Run `git pull origin main` before you start working or pushing to avoid merge conflicts.
- **Never commit virtual environments:** Make sure your `venv/` folder stays inside `.gitignore`.
- **Write clear commit messages:** Keep commits descriptive (e.g., `git commit -m "add vendor input validation"` instead of `update`).

---

### Timeline & Deadlines

- **Week 1 & 2:** ER diagram, table schemas, sample seed data, and UI prototype. _(Done)_
- **Week 3:** Connect Streamlit directly to MySQL and replace mock lists with real `INSERT` and `SELECT` queries. _(Next step)_
- **Week 4:** Stored procedures for claiming food, automated triggers for expired food, and admin views.
- **Week 5:** Final testing, bug fixing, and lab defense.
