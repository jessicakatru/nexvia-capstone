import pandas as pd
import streamlit as st
from sqlalchemy import create_engine

st.set_page_config(page_title="Supply Chain Control Tower", layout="wide")
engine = create_engine("postgresql+psycopg2://supply:supply@localhost:5432/supplychain")

def q(sql):
    return pd.read_sql(sql, engine)

st.title("Retail and Supply Chain Control Tower")
st.caption("Synthetic data. Postgres, Airflow hourly refresh, Prophet forecast, z-score anomalies.")

stock = q("select * from kpi_days_of_inventory")
sup = q("select * from kpi_supplier_delivery")
so = q("select avg(stockout_rate_pct) as v from kpi_stockout_rate").iloc[0, 0]
fc = q("select * from demand_forecast")

c1, c2, c3, c4 = st.columns(4)
c1.metric("Avg stock-out rate", f"{so:.1f}%")
c2.metric("Avg on-time delivery", f"{sup['on_time_pct'].mean():.1f}%")
c3.metric("Avg supplier lead time", f"{sup['avg_lead_days'].mean():.1f} days")
c4.metric("Median days of inventory", f"{stock['days_of_inventory'].median():.1f}")

l, r = st.columns(2)
with l:
    st.subheader("Supplier on-time delivery %")
    st.bar_chart(sup.set_index("name")["on_time_pct"].astype(float))
with r:
    st.subheader("Days of inventory (lowest 15)")
    st.bar_chart(stock.nsmallest(15, "days_of_inventory").set_index("product_id")["days_of_inventory"])

st.subheader("Demand forecast vs current stock")
st.dataframe(fc.sort_values("days_of_cover"), use_container_width=True)

st.subheader("What-if: supplier delay")
sid = st.selectbox("Supplier", sup["supplier_id"].tolist())
delay = st.slider("Extra delay (days)", 0, 14, 7)
w = q(f"""select p.product_id, k.stock_level, k.days_of_inventory, s.lead_days
          from products p
          join kpi_days_of_inventory k using (product_id)
          join suppliers s using (supplier_id)
          where p.supplier_id = {int(sid)}""")
w["new_lead_days"] = w["lead_days"] + delay
w["at_risk"] = w["days_of_inventory"] < w["new_lead_days"]
st.write(f"{int(w['at_risk'].sum())} of {len(w)} products would run out before the delayed shipment arrives.")
st.dataframe(w, use_container_width=True)

st.subheader("Latest alerts")
st.dataframe(q("select * from alerts_log order by ts desc limit 20"), use_container_width=True)
