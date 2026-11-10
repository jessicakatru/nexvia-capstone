import pandas as pd
import numpy as np
import random
import os
from datetime import timedelta

random.seed(42)
np.random.seed(42)

RAW = "data/raw/"
OUT = "data/generated/"

orders = pd.read_csv(RAW + "olist_orders_dataset.csv",
                     parse_dates=["order_purchase_timestamp"])
customers = pd.read_csv(RAW + "olist_customers_dataset.csv")
orders = orders.merge(customers[["customer_id", "customer_unique_id"]], on="customer_id")
orders = orders.sample(20000, random_state=42)  # subset, fast ga untundi

channels = ["google_ads", "facebook_ads", "email", "organic", "affiliate", "direct"]
weights = [0.25, 0.2, 0.15, 0.2, 0.1, 0.1]

sessions = []
sid = 1
for _, o in orders.iterrows():
    n = random.randint(1, 4)  # purchase mundu entha sessions
    for i in range(n):
        ts = o["order_purchase_timestamp"] - timedelta(
            days=(n - i - 1) * random.randint(1, 5),
            hours=random.randint(0, 5))
        sessions.append({
            "session_id": sid,
            "customer_unique_id": o["customer_unique_id"],
            "session_start": ts,
            "channel": np.random.choice(channels, p=weights),
            "converted_order_id": o["order_id"] if i == n - 1 else None,
        })
        sid += 1

sessions = pd.DataFrame(sessions)

# ad spend: roju, channel wise
days = pd.date_range(sessions.session_start.min().date(),
                     sessions.session_start.max().date())
paid = ["google_ads", "facebook_ads", "email", "affiliate"]
spend = pd.DataFrame([
    {"date": d, "channel": c, "spend": round(np.random.uniform(50, 400), 2)}
    for d in days for c in paid
])

os.makedirs(OUT, exist_ok=True)
sessions.to_csv(OUT + "sessions.csv", index=False)
spend.to_csv(OUT + "ad_spend.csv", index=False)
print(len(sessions), "sessions,", len(spend), "spend rows")