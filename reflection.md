# Reflection

## What I built

Two projects for the Data Analytics track.

- **DA-02:** a pipeline from raw data to a Tableau dashboard. Data goes into BigQuery, dbt models clean it, then build customer RFM segments, four attribution models (first touch, last touch, linear, time-decay) and campaign ROI and CPA.
- **DA-03:** a supply chain control tower. PostgreSQL holds inventory, shipments and suppliers. An Airflow DAG refreshes data every hour. SQL views calculate KPIs, z-score finds anomalies, Prophet forecasts demand, and a Streamlit dashboard shows everything with a what-if panel.

## What I owned

- Set up both repos, the BigQuery dataset, the dbt project and the Docker setup
- Wrote and debugged the SQL models, the data generators, the forecast, the alerts and the dashboards
- Fixed the problems that came up (below) and documented the decisions in the READMEs

## What went wrong and how I fixed it

- **Wrong file in a BigQuery table.** My `orders` table had the customers file inside it. dbt gave "unrecognized name: order_id", which led me to check the table schema. I reloaded the correct file with a short Python script.
- **Python 3.14 and dbt.** The install failed with SSL and build errors. I moved to a Python 3.12 virtual environment and installed a prebuilt `cryptography` package.
- **Docker did not run on my Intel Mac.** The Docker version I installed first was not supported. I used GitHub Codespaces instead, where Docker works.
- **Empty chart.** The supplier chart showed no bars because the column had the wrong data type. I cast it to float.

## What I learned

- Check the data first. Most of my errors came from bad input, not bad code.
- dbt makes SQL work easier to read, test and rerun.
- Attribution models can give different credit to the same channel, so the choice of model matters.
- A scheduler like Airflow is what turns a script into a pipeline.
- Writing the README and noting the limits (synthetic data, Streamlit instead of Superset) made the work easier to trust.

## Limits and what I would do next

- Sessions, ad spend and all DA-03 data are synthetic, so the results show the pipelines working and are not real business findings.
- Slack alerts are written but not connected to a real webhook.
- Next: connect real data, add dbt tests, and set up proper alerting.