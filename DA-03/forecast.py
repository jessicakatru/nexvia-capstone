import logging
import pandas as pd
from sqlalchemy import create_engine
from prophet import Prophet

logging.getLogger("cmdstanpy").setLevel(logging.ERROR)
logging.getLogger("prophet").setLevel(logging.ERROR)

engine = create_engine("postgresql+psycopg2://supply:supply@localhost:5432/supplychain")
inv = pd.read_sql("select ts, product_id, stock_level, units_sold from inventory_hourly", engine)
inv["day"] = inv["ts"].dt.floor("D")

daily = inv.groupby(["product_id", "day"])["units_sold"].sum().reset_index()
# first and last day are partial, drop them
daily = daily[(daily["day"] > daily["day"].min()) & (daily["day"] < daily["day"].max())]
latest = inv.sort_values("ts").groupby("product_id").last()["stock_level"]

rows = []
for pid in sorted(daily["product_id"].unique())[:15]:
    d = daily[daily["product_id"] == pid][["day", "units_sold"]]
    d.columns = ["ds", "y"]
    m = Prophet(daily_seasonality=False, weekly_seasonality=False, yearly_seasonality=False)
    m.fit(d)
    f = m.predict(m.make_future_dataframe(periods=7))
    pred_7d = float(f.tail(7)["yhat"].clip(lower=0).sum())
    stock = int(latest[pid])
    rows.append({
        "product_id": int(pid),
        "current_stock": stock,
        "forecast_7d_demand": round(pred_7d),
        "days_of_cover": round(stock / (pred_7d / 7), 1) if pred_7d > 0 else None,
        "status": "STOCKOUT RISK" if stock < pred_7d else "OK",
    })

out = pd.DataFrame(rows)
out.to_sql("demand_forecast", engine, if_exists="replace", index=False)
print(out.sort_values("days_of_cover").to_string(index=False))