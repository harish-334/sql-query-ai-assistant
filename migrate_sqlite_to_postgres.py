"""
Migrate tables from local normalized.db (SQLite) into a PostgreSQL database.

Usage:
  1) Make sure your environment variables are set (we'll load them into the terminal later).
  2) Activate virtualenv and run:
       python migrate_sqlite_to_postgres.py

Notes:
 - This script uses pandas.to_sql (SQLAlchemy) to copy data.
 - It then creates sequences for integer primary-key-like columns ending with "ID".
 - It finally attempts to add foreign key constraints commonly used in the mini-project.
 - Be careful: if tables with the same name exist in Postgres they will be replaced.
"""

import os
import sqlite3
import pandas as pd
from sqlalchemy import create_engine, text
from urllib.parse import quote_plus

POSTGRES_USERNAME = os.environ.get("POSTGRES_USERNAME") or "your_pg_user"
POSTGRES_PASSWORD = os.environ.get("POSTGRES_PASSWORD") or "your_pg_password"
POSTGRES_SERVER = os.environ.get("POSTGRES_SERVER") or "your_render_host:5432"
POSTGRES_DATABASE = os.environ.get("POSTGRES_DATABASE") or "your_db_name"

SQLITE_PATH = "normalized.db" 

if not os.path.exists(SQLITE_PATH):
    raise SystemExit(f"SQLite DB not found at {SQLITE_PATH}. Put normalized.db in the script folder.")

pg_url = f"postgresql://{POSTGRES_USERNAME}:{quote_plus(POSTGRES_PASSWORD)}@{POSTGRES_SERVER}/{POSTGRES_DATABASE}"
print("Postgres URL (constructed):", pg_url.split("@")[0] + "@<host>/" + POSTGRES_DATABASE)

engine = create_engine(pg_url, future=True)

sconn = sqlite3.connect(SQLITE_PATH)
cursor = sconn.cursor()
cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%';")
tables = [row[0] for row in cursor.fetchall()]
print("SQLite tables found:", tables)

# 1) Copy each table over
for table in tables:
    print(f"\nMigrating table: {table} ...")
    df = pd.read_sql_query(f"SELECT * FROM \"{table}\";", sconn)
    # Write to Postgres (if_exists='replace' will drop and recreate)
    df.to_sql(table, engine, if_exists='replace', index=False)
    print(f"  -> {len(df)} rows written to Postgres table '{table}'")

# 2) For integer PK-like columns ending with ID, create sequences and set default
with engine.connect() as conn:
    for table in tables:
        q = text(f"""
            SELECT column_name, data_type
            FROM information_schema.columns
            WHERE table_name = :tbl
        """)
        res = conn.execute(q, {"tbl": table})
        cols = res.fetchall()
        for col_name, data_type in cols:
            if col_name.lower().endswith("id") and data_type in ("integer", "bigint", "smallint"):
                seq_name = f"{table.lower()}_{col_name.lower()}_seq"
                print(f"Setting up sequence for {table}.{col_name} -> {seq_name}")
                try:
                    conn.execute(text(f"CREATE SEQUENCE IF NOT EXISTS {seq_name};"))
                except Exception as e:
                    print("  create sequence failed:", e)
                try:
                    conn.execute(text(f"ALTER TABLE \"{table}\" ALTER COLUMN \"{col_name}\" SET DEFAULT nextval('{seq_name}');"))
                except Exception as e:
                    print("  alter default failed:", e)
                try:
                    max_val = conn.execute(text(f"SELECT COALESCE(MAX(\"{col_name}\"), 0) FROM \"{table}\";")).scalar_one()
                    next_val = int(max_val) + 1
                    conn.execute(text(f"SELECT setval('{seq_name}', {next_val}, false);"))
                    print(f"  sequence {seq_name} set to {next_val}")
                except Exception as e:
                    print("  set sequence value failed:", e)

# 3) Optionally add FK constraints for known relationships (adjust if your schema differs)
fk_statements = [
    # country.RegionID -> Region.RegionID
    "ALTER TABLE country ADD CONSTRAINT fk_country_region FOREIGN KEY (regionid) REFERENCES region(regionid);",
    # customer.CountryID -> Country.CountryID
    "ALTER TABLE customer ADD CONSTRAINT fk_customer_country FOREIGN KEY (countryid) REFERENCES country(countryid);",
    # product.ProductCategoryID -> ProductCategory.ProductCategoryID
    "ALTER TABLE product ADD CONSTRAINT fk_product_productcategory FOREIGN KEY (productcategoryid) REFERENCES productcategory(productcategoryid);",
    # orderdetail.CustomerID -> Customer.CustomerID
    "ALTER TABLE orderdetail ADD CONSTRAINT fk_orderdetail_customer FOREIGN KEY (customerid) REFERENCES customer(customerid);",
    # orderdetail.ProductID -> Product.ProductID
    "ALTER TABLE orderdetail ADD CONSTRAINT fk_orderdetail_product FOREIGN KEY (productid) REFERENCES product(productid);",
]

with engine.connect() as conn:
    for stmt in fk_statements:
        try:
            print("Adding FK:", stmt)
            conn.execute(text(stmt))
        except Exception as e:
            print("  Could not add FK (maybe already present or column/table missing):", e)

print("\nMigration complete. Verify tables in Render dashboard or by connecting with psql.")
sconn.close()
