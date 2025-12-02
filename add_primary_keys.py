import os
from sqlalchemy import create_engine, text
from urllib.parse import quote_plus

user = os.getenv("POSTGRES_USERNAME")
pwd  = os.getenv("POSTGRES_PASSWORD")
server = os.getenv("POSTGRES_SERVER")
db = os.getenv("POSTGRES_DATABASE")

pg_url = f"postgresql://{user}:{quote_plus(pwd)}@{server}/{db}"
engine = create_engine(pg_url, future=True)

pk_statements = [
    ('Region', 'RegionID'),
    ('Country', 'CountryID'),
    ('Customer', 'CustomerID'),
    ('ProductCategory', 'ProductCategoryID'),
    ('Product', 'ProductID'),
]

with engine.begin() as conn:
    for table, col in pk_statements:
        try:
            print(f"Adding PRIMARY KEY on {table}({col}) ...")
            conn.execute(text(f'ALTER TABLE "{table}" ADD PRIMARY KEY ("{col}");'))
            print("  ✔ Success")
        except Exception as e:
            print(f"  ⚠ Failed: {e}")

print("\nDone adding primary keys.")
