import numpy as np, psycopg2
from psycopg2.extras import execute_values
from datetime import datetime, timedelta

rng = np.random.default_rng(42)
conn = psycopg2.connect(host="localhost", port=5432, user="supply",
                        password="supply", dbname="supplychain")
cur = conn.cursor()
cur.execute("""
DROP TABLE IF EXISTS shipments, inventory_hourly, products, suppliers CASCADE;
CREATE TABLE suppliers (supplier_id INT PRIMARY KEY, name TEXT, lead_days INT);
CREATE TABLE products (product_id INT PRIMARY KEY, name TEXT, supplier_id INT, reorder_point INT);
CREATE TABLE inventory_hourly (ts TIMESTAMP, product_id INT, stock_level INT, units_sold INT);
CREATE TABLE shipments (shipment_id INT PRIMARY KEY, supplier_id INT, product_id INT,
  ordered_at TIMESTAMP, promised_at TIMESTAMP, delivered_at TIMESTAMP, qty INT);
""")

N_SUP, N_PROD, DAYS = 20, 50, 14
sup = [(i + 1, f"Supplier {i+1}", int(rng.integers(2, 9))) for i in range(N_SUP)]
execute_values(cur, "INSERT INTO suppliers VALUES %s", sup)
prod_sup = rng.integers(1, N_SUP + 1, N_PROD)
reorder = rng.integers(80, 150, N_PROD)
prods = [(i + 1, f"Product {i+1}", int(prod_sup[i]), int(reorder[i])) for i in range(N_PROD)]
execute_values(cur, "INSERT INTO products VALUES %s", prods)

end = datetime.now().replace(minute=0, second=0, microsecond=0)
start = end - timedelta(days=DAYS)
hours = DAYS * 24
stock = rng.integers(200, 500, N_PROD)
base = rng.uniform(1, 6, N_PROD)
spike = set(rng.choice(N_PROD, 5, replace=False).tolist())
pending, rows = {}, []
for h in range(hours):
    ts = start + timedelta(hours=h)
    f = 1.6 if 9 <= ts.hour <= 21 else 0.4
    for p in range(N_PROD):
        m = 3 if (h >= hours - 48 and p in spike) else 1
        sold = int(min(rng.poisson(base[p] * f * m), stock[p]))
        stock[p] -= sold
        if p in pending and h >= pending[p]:
            stock[p] += 300
            del pending[p]
        if stock[p] < reorder[p] and p not in pending:
            pending[p] = h + int(rng.integers(24, 96))
        rows.append((ts, p + 1, int(stock[p]), sold))
execute_values(cur, "INSERT INTO inventory_hourly VALUES %s", rows)

late_sup = {3, 7}
ships = []
for i in range(1500):
    s = int(rng.integers(1, N_SUP + 1))
    p = int(rng.choice(np.where(prod_sup == s)[0]) + 1) if (prod_sup == s).any() else 1
    ordered = start + timedelta(hours=int(rng.integers(0, hours)))
    promised = ordered + timedelta(days=sup[s - 1][2])
    delay = max(-1.0, float(rng.normal(0.5, 1.0)))
    if s in late_sup and ordered > end - timedelta(days=5):
        delay += float(rng.uniform(3, 5))
    delivered = promised + timedelta(days=delay)
    if delivered > end:
        delivered = None
    ships.append((i + 1, s, p, ordered, promised, delivered, int(rng.integers(100, 400))))
execute_values(cur, "INSERT INTO shipments VALUES %s", ships)
conn.commit()
for t in ["suppliers", "products", "inventory_hourly", "shipments"]:
    cur.execute(f"SELECT COUNT(*) FROM {t}")
    print(t, cur.fetchone()[0])
