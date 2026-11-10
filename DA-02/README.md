# DA-02: Customer 360 and Marketing Attribution

This project combines website sessions, orders and ad spend into one customer view, then works out which marketing channels actually bring in revenue.

I'm building this as part of my Data Analytics internship at Nexvia Technologies.

## What I'm building

1. Load the Olist e-commerce dataset into BigQuery
2. Generate sessions and ad-spend data with Python
3. Link sessions to customers (identity resolution)
4. Build dbt models: sessions, orders, customer profile
5. Calculate RFM scores and customer lifetime value, then segment customers
6. Build 4 attribution models (first touch, last touch, linear, time-decay) and compare them
7. Calculate campaign ROI and cost per acquisition
8. Make a Tableau dashboard with budget recommendations

## Tech stack

BigQuery, dbt, Python, SQL, Tableau

## Dataset

Olist Brazilian E-Commerce (Kaggle). Sessions and ad spend are synthetic, generated with generate_data.py.

## Status

Work in progress.

- [x] Data generation script
- [ ] Data loaded into BigQuery
- [ ] dbt models
- [ ] RFM and CLV
- [ ] Attribution models
- [ ] ROI and CPA
- [ ] Dashboard

## Author

Jessica Katru
