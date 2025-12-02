"""
Safer FK adder:
 - Runs orphan checks with a short-lived read connection
 - If no orphans, opens a fresh transactional connection (engine.begin()) to add FK
 - Prints clear messages
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

def count_orphans(conn, child, child_col, parent, parent_col):
    q = text(f'''
        SELECT COUNT(*) FROM "{child}" c
        LEFT JOIN "{parent}" p ON c."{child_col}" = p."{parent_col}"
        WHERE p."{parent_col}" IS NULL
    ''')
    return conn.execute(q).scalar_one()

def sample_orphans(conn, child, child_col, parent, parent_col, limit=5):
    q = text(f'''
        SELECT c.* FROM "{child}" c
        LEFT JOIN "{parent}" p ON c."{child_col}" = p."{parent_col}"
        WHERE p."{parent_col}" IS NULL
        LIMIT :lim
    ''')
    rows = conn.execute(q, {"lim": limit}).fetchall()
    return rows

print("Connecting to Postgres and checking foreign-key readiness...\n")

for name, child, child_col, parent, parent_col in fks:
    # 1) check orphans using a short-lived (read) connection
    with engine.connect() as read_conn:
        try:
            cnt = count_orphans(read_conn, child, child_col, parent, parent_col)
        except Exception as e:
            print(f"ERROR checking orphans for {child}.{child_col} -> {parent}.{parent_col}: {e}")
            print("Skipping this FK and continuing.")
            continue

    print(f"Checked {child}.{child_col} -> {parent}.{parent_col}: Orphan count = {cnt}")

    if cnt > 0:
        # show sample rows to help fix
        with engine.connect() as read_conn:
            samples = sample_orphans(read_conn, child, child_col, parent, parent_col, limit=5)
        print(f"  Sample orphan rows from {child} (up to 5):")
        for s in samples:
            print("   ", tuple(s))
        print(f"  => Cannot add FK {name} until those orphans are resolved. Aborting further FK creation.\n")
        break

    # 2) no orphans -> add FK in its own transaction using engine.begin()
    alter_sql = f'ALTER TABLE "{child}" ADD CONSTRAINT {name} FOREIGN KEY ("{child_col}") REFERENCES "{parent}"("{parent_col}");'
    try:
        with engine.begin() as tx_conn:   # fresh transactional connection
            tx_conn.execute(text(alter_sql))
        print(f"  Added FK {name} successfully.\n")
    except Exception as e:
        print(f"  FAILED to add FK {name}: {e}\n")
        # continue to next FK (we don't abort entirely)
        continue

print("FK check/add process complete. Inspect output above for any failures or orphan samples.")
