# Nexvia Capstone Projects

Data Analytics track, Nexvia Technologies internship.

## Projects

| Project | What it does | Stack |
|---|---|---|
| [DA-02](DA-02/) Customer 360 and Marketing Attribution | Combines sessions, orders and ad spend, segments customers (RFM), compares 4 attribution models, calculates channel ROI and CPA | BigQuery, dbt, Python, Tableau |
| [DA-03](DA-03/) Retail and Supply Chain Control Tower | Hourly inventory refresh, KPIs, anomaly detection, demand forecast, alerts, what-if dashboard | PostgreSQL, Airflow, Docker, Prophet, Streamlit |

**Live dashboard (DA-02):** https://public.tableau.com/app/profile/jessica.katru/viz/MarketingAttribution_17945677282420/Dashboard1

## Notes

- Orders and payments in DA-02 come from the Olist Brazilian E-Commerce dataset (Kaggle). Sessions, ad spend and all DA-03 data are synthetic, so results show the pipelines working and are not real business findings.
- DA-03 uses Streamlit instead of Superset to keep setup light.

## Structure

- `DA-02/` : data generation, dbt project, architecture doc
- `DA-03/` : Docker compose, Airflow DAG, SQL, forecast, alerts, dashboard
- `reflection.md` : what I learned and what I owned

## Author

Jessica Katru