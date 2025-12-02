"""
Check parent tables for NULLs / duplicates so we can safely add PK/UNIQUE constraints.
Run in the same environment where POSTGRES_* env vars are set.
"""

import os
from sqlalchemy import create_engine, text
from urllib.parse import quote_plus

user = os.getenv("POSTGRES_USERNAME")
pwd  = os.getenv("POSTGRES_PASSWORD")
server = os.getenv("POSTGRES_SERVER")
db = os.getenv("POSTGRES_DATABASE")

if not all([user, pwd, server, db]):
    raise SystemExit("Set POSTGRES_USERNAME, POSTGRES_PASSWORD, POSTGRES_SERVER, POSTGRES_DATABASE in environment")

pg_url = f"postgresql://{user}:{quote_plus(pwd)}@{server}/{db}"
engine = create_engine(pg_url, future=True)

# parent columns we need to check: (table, id_column)
parents = [
    ("Region", "RegionID"),
    ("Country", "CountryID"),
    ("Customer", "CustomerID"),
    ("ProductCategory", "ProductCategoryID"),
    ("Product", "ProductID"),
]

def run_check(conn, table, col):
    print(f"\nChecking {table}.{col}")
    total = conn.execute(text(f'SELECT COUNT(*) FROM "{table}";')).scalar_one()
    nulls = conn.execute(text(f'SELECT COUNT(*) FROM "{table}" WHERE "{col}" IS NULL;')).scalar_one()
    distinct = conn.execute(text(f'SELECT COUNT(DISTINCT "{col}") FROM "{table}";')).scalar_one()
    dup_count = total - distinct
    print(f"  total rows = {total}")
    print(f"  NULL {col} = {nulls}")
    print(f"  distinct {col} = {distinct}")
    print(f"  duplicate keys (total - distinct) = {dup_count}")
    if dup_count > 0:
        print("  Showing up to 5 duplicate key examples (value, occurrences):")
        q = text(f'''
            SELECT "{col}", COUNT(*) AS cnt
            FROM "{table}"
            GROUP BY "{col}"
            HAVING COUNT(*) > 1
            ORDER BY cnt DESC
            LIMIT 5;
        ''')
        rows = conn.execute(q).fetchall()
        for r in rows:
            print("   ", tuple(r))
    if nulls > 0:
        q2 = text(f'SELECT * FROM "{table}" WHERE "{col}" IS NULL LIMIT 5;')
        rows = conn.execute(q2).fetchall()
        print("  Sample rows with NULL id (up to 5):")
        for r in rows:
            print("   ", tuple(r))

with engine.connect() as conn:
    print("Connected to Postgres - checking parent key columns.")
    for table, col in parents:
        try:
            run_check(conn, table, col)
        except Exception as e:
            print(f"  ERROR checking {table}.{col}: {e}")

print("\nChecks complete. If all parents have 0 NULLs and 0 duplicate keys, tell me and I'll provide the SQL to add PRIMARY KEY / UNIQUE constraints and then re-run FK creation.")
