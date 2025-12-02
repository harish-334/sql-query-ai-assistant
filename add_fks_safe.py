"""
Safely check for orphan rows and add FK constraints for the migrated tables.
Run in the same environment where POSTGRES_* env vars are set.

It will:
 - check for orphans for each FK
 - if no orphans, attempt to add the FK (in its own transaction)
 - print a summary
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

# FK definitions: (constraint_name, child_table, child_col, parent_table, parent_col)
fks = [
    ("fk_country_region", "Country", "RegionID", "Region", "RegionID"),
    ("fk_customer_country", "Customer", "CountryID", "Country", "CountryID"),
    ("fk_product_productcategory", "Product", "ProductCategoryID", "ProductCategory", "ProductCategoryID"),
    ("fk_orderdetail_customer", "OrderDetail", "CustomerID", "Customer", "CustomerID"),
    ("fk_orderdetail_product", "OrderDetail", "ProductID", "Product", "ProductID"),
]

def check_orphans(conn, child, child_col, parent, parent_col, sample_limit=5):
    # returns (count, samples_list)
    q_count = text(f'''
        SELECT COUNT(*) FROM "{child}" c
        LEFT JOIN "{parent}" p ON c."{child_col}" = p."{parent_col}"
        WHERE p."{parent_col}" IS NULL
    ''')
    cnt = conn.execute(q_count).scalar_one()
    samples = []
    if cnt > 0:
        q_sample = text(f'''
            SELECT c.* FROM "{child}" c
            LEFT JOIN "{parent}" p ON c."{child_col}" = p."{parent_col}"
            WHERE p."{parent_col}" IS NULL
            LIMIT :lim
        ''')
        rows = conn.execute(q_sample, {"lim": sample_limit}).fetchall()
        samples = [tuple(row) for row in rows]
    return cnt, samples

def add_fk(conn, stmt):
    conn.execute(text(stmt))

with engine.connect() as conn:
    print("Connected to Postgres. Verifying FK readiness...\n")
    for name, child, child_col, parent, parent_col in fks:
        print(f"Checking orphans for {child}.{child_col} -> {parent}.{parent_col} ...")
        cnt, samples = check_orphans(conn, child, child_col, parent, parent_col)
        print(f"  Orphan count = {cnt}")
        if cnt > 0:
            print(f"  Sample orphan rows from {child}:")
            for s in samples:
                print("   ", s)
            print(f"\n  => Cannot add FK {name} until orphans are resolved. Aborting further FK creation.\n")
            break

        # no orphans: attempt to add constraint in its own transaction
        alter_sql = f'ALTER TABLE "{child}" ADD CONSTRAINT {name} FOREIGN KEY ("{child_col}") REFERENCES "{parent}"("{parent_col}");'
        try:
            print(f"  Adding FK {name} ...")
            with conn.begin():  # separate transaction
                add_fk(conn, alter_sql)
            print("  OK")
        except Exception as e:
            # show the error but continue to next FK
            print("  FAILED to add FK:", e)
            print("  (Continuing to next FK)\n")

    print("\nDone. If any FK failed or orphans were found, fix them and re-run this script.")
