import os
import numpy as np
import psycopg2
from datetime import timedelta

rng = np.random.default_rng()
conn = psycopg2.connect(host=os.getenv("PGHOST", "localhost"), port=5432, user="supply",
                        password="supply", dbname="supplychain")
cur = conn.cursor()

cur.execute("select max(ts) from inventory_hourly")
last_ts = cur.fetchone()[0]
new_ts = last_ts + timedelta(hours=1)

cur.execute("""
    select p.product_id, p.reorder_point, i.stock_level,
           (select coalesce(avg(units_sold), 2) from inventory_hourly h
             where h.product_id = p.product_id
               and h.ts > %s - interval '7 days') as avg_sold
    from products p
    join inventory_hourly i on i.product_id = p.product_id and i.ts = %s
""", (last_ts, last_ts))

rows = []
for pid, reorder, stock, avg_sold in cur.fetchall():
    sold = int(min(rng.poisson(float(avg_sold)), stock))
    stock -= sold
    if stock < reorder and rng.random() < 0.15:
        stock += 300
    rows.append((new_ts, pid, int(stock), sold))

cur.executemany("insert into inventory_hourly values (%s, %s, %s, %s)", rows)
conn.commit()
print(f"Added {len(rows)} rows for {new_ts}")