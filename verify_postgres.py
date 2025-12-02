import os
from sqlalchemy import create_engine, inspect
from urllib.parse import quote_plus

user = os.getenv("POSTGRES_USERNAME")
pwd  = os.getenv("POSTGRES_PASSWORD")
server = os.getenv("POSTGRES_SERVER")
db = os.getenv("POSTGRES_DATABASE")

if not all([user, pwd, server, db]):
    raise SystemExit("Set POSTGRES_USERNAME, POSTGRES_PASSWORD, POSTGRES_SERVER, POSTGRES_DATABASE in environment")

pg_url = f"postgresql://{user}:{quote_plus(pwd)}@{server}/{db}"
engine = create_engine(pg_url, future=True)

insp = inspect(engine)
tables = insp.get_table_names(schema='public')
print("Tables in Postgres (schema=public):", tables)

for t in tables:
    cols = insp.get_columns(t, schema='public')
    print(f"\nTable: {t}")
    for c in cols:
        print("  ", c['name'], c['type'])
    # show up to 3 sample rows
    with engine.connect() as conn:
        try:
            rows = conn.execute(f'SELECT * FROM "{t}" LIMIT 3;').fetchall()
            print("  Sample rows:", rows)
        except Exception as e:
            print("  Could not fetch sample rows:", e)
