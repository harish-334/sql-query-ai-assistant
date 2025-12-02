import sqlite3
import pandas as pd
import os
db = "normalized.db"

print("cwd:", os.getcwd())
print("exists:", os.path.exists(db))

if not os.path.exists(db):
    print("ERROR: normalized.db not found in project root.")
    raise SystemExit(1)

conn = sqlite3.connect(db)
print("\nTables:")
print(pd.read_sql_query("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name;", conn).to_string(index=False))
print("\nSample OrderDetail (5 rows):")
try:
    print(pd.read_sql_query("SELECT * FROM OrderDetail LIMIT 5;", conn).to_string(index=False))
except Exception as e:
    print("Could not read OrderDetail:", e)
conn.close()
