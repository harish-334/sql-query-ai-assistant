from sqlalchemy import create_engine, text
import os
from urllib.parse import quote_plus

u=os.getenv("POSTGRES_USERNAME")
p=quote_plus(os.getenv("POSTGRES_PASSWORD"))
s=os.getenv("POSTGRES_SERVER")
d=os.getenv("POSTGRES_DATABASE")

engine = create_engine(f"postgresql://{u}:{p}@{s}/{d}", future=True)

with engine.connect() as conn:
    rows = conn.execute(text('SELECT COUNT(*) FROM "OrderDetail";')).fetchall()
    print(rows)
