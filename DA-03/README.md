# DA-03: Retail and Supply Chain Control Tower

A near real-time view of inventory, deliveries and suppliers. The goal is to catch problems like stock-outs and late suppliers before they hurt sales.

Part of my Data Analytics internship at Nexvia Technologies.

## What I'm building

1. Store inventory, shipment and supplier data in PostgreSQL
2. Refresh the data every hour using an Airflow DAG
3. Track KPIs: stock-out rate, on-time delivery, supplier lead time, days of inventory
4. Detect anomalies using z-score
5. Forecast demand with Prophet and compare it with current stock
6. Build a Superset dashboard with a what-if panel
7. Send Slack or email alerts when a threshold is crossed

## Tech stack

PostgreSQL, Airflow, Python, Prophet, Apache Superset, Docker

## Status

Work in progress.

## Author

Jessica Katru
