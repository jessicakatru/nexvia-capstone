import os, json, urllib.request
import psycopg2

conn = psycopg2.connect(host=os.getenv("PGHOST", "localhost"), port=5432,
                        user="supply", password="supply", dbname="supplychain")
cur = conn.cursor()
cur.execute("""CREATE TABLE IF NOT EXISTS alerts_log
               (ts TIMESTAMP DEFAULT now(), alert_type TEXT, message TEXT)""")

alerts = []

cur.execute("select product_id, current_stock, forecast_7d_demand from demand_forecast where status = 'STOCKOUT RISK'")
for pid, stock, fc in cur.fetchall():
    alerts.append(("STOCKOUT_RISK", f"Product {pid}: stock {stock}, forecast 7d demand {fc}"))

cur.execute("select product_id, z_score from anomaly_demand")
for pid, z in cur.fetchall():
    alerts.append(("DEMAND_SPIKE", f"Product {pid}: demand spike, z-score {z}"))

cur.execute("select supplier_id, avg_delay_days from anomaly_supplier_delay")
for sid, d in cur.fetchall():
    alerts.append(("SUPPLIER_DELAY", f"Supplier {sid}: avg delay {d} days"))

for t, m in alerts:
    cur.execute("insert into alerts_log (alert_type, message) values (%s, %s)", (t, m))
conn.commit()

summary = f"Supply chain alerts: {len(alerts)}\n" + "\n".join(f"[{t}] {m}" for t, m in alerts[:20])
print(summary)

hook = os.getenv("SLACK_WEBHOOK_URL")
if hook:
    req = urllib.request.Request(hook, data=json.dumps({"text": summary}).encode(),
                                 headers={"Content-Type": "application/json"})
    urllib.request.urlopen(req)
    print("Sent to Slack")
else:
    print("(No SLACK_WEBHOOK_URL set, alerts saved to alerts_log table only)")