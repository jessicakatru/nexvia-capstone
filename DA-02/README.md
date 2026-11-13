# DA-02: Customer 360 and Marketing Attribution

I combined website sessions, orders and ad spend into one customer view, then measured which marketing channels bring in revenue.

**Live dashboard:** https://public.tableau.com/app/profile/jessica.katru/viz/MarketingAttribution_17945677282420/Dashboard1

**Note:** Orders and payments come from the Olist Brazilian E-Commerce dataset (Kaggle). Sessions and ad spend are synthetic, generated with `generate_data.py`, so the channel numbers below show the pipeline working and are not real business findings.

## Pipeline

1. `generate_data.py` creates synthetic sessions and ad spend from Olist orders
2. Data loaded into BigQuery (`capstone` dataset)
3. dbt staging models: orders, customers, payments, sessions
4. dbt marts: `customer_profile`, `customer_rfm`, `touchpoints`, `attribution_by_channel`, `campaign_roi`
5. Tableau Public dashboard on top of `campaign_roi`

## What I built

- **RFM segmentation:** recency, frequency and monetary scores (1 to 5) with segments: Champions, Loyal, New Customers, At Risk, Lost, Potential
- **4 attribution models:** first touch, last touch, linear, time-decay (7-day half-life)
- **Campaign ROI and CPA** per channel

## Results (time-decay attribution)

| Channel | Spend | Conversions | CPA | ROI |
|---|---|---|---|---|
| google_ads | 169,030 | 5,279 | 32.02 | 4.06 |
| facebook_ads | 169,482 | 4,102 | 41.32 | 2.87 |
| email | 168,998 | 3,068 | 55.08 | 1.78 |
| affiliate | 173,608 | 2,038 | 85.19 | 0.85 |

**Recommendation:** shift budget from affiliate (lowest ROI, highest CPA) to Google Ads (highest ROI, lowest CPA).

## Tech stack

BigQuery, dbt, Python, SQL, Tableau Public

## How to run

```bash
cd DA-02
python generate_data.py        # needs Olist CSVs in data/raw/
# load CSVs into BigQuery dataset "capstone", then:
cd dbt_project
dbt run
```

## Status

- [x] Data generation and BigQuery load
- [x] dbt models
- [x] RFM and CLV segments
- [x] Attribution models
- [x] ROI and CPA
- [x] Tableau dashboard
- [ ] Architecture diagram
- [ ] Demo video

## Author

Jessica Katru
