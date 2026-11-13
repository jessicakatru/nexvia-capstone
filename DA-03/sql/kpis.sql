CREATE OR REPLACE VIEW kpi_stockout_rate AS
SELECT product_id,
       ROUND(100.0 * AVG((stock_level = 0)::int), 2) AS stockout_rate_pct
FROM inventory_hourly
GROUP BY product_id;

CREATE OR REPLACE VIEW kpi_supplier_delivery AS
SELECT s.supplier_id, s.name,
       COUNT(*) AS delivered_shipments,
       ROUND(100.0 * AVG((sh.delivered_at <= sh.promised_at)::int), 1) AS on_time_pct,
       ROUND(AVG(EXTRACT(EPOCH FROM (sh.delivered_at - sh.ordered_at)) / 86400)::numeric, 2) AS avg_lead_days
FROM shipments sh
JOIN suppliers s ON s.supplier_id = sh.supplier_id
WHERE sh.delivered_at IS NOT NULL
GROUP BY s.supplier_id, s.name;

CREATE OR REPLACE VIEW kpi_days_of_inventory AS
WITH latest AS (
    SELECT DISTINCT ON (product_id) product_id, stock_level
    FROM inventory_hourly
    ORDER BY product_id, ts DESC
),
daily AS (
    SELECT product_id, SUM(units_sold) / 7.0 AS avg_daily_sales
    FROM inventory_hourly
    WHERE ts > (SELECT MAX(ts) FROM inventory_hourly) - INTERVAL '7 days'
    GROUP BY product_id
)
SELECT l.product_id, l.stock_level,
       ROUND(d.avg_daily_sales::numeric, 1) AS avg_daily_sales,
       ROUND((l.stock_level / NULLIF(d.avg_daily_sales, 0))::numeric, 1) AS days_of_inventory
FROM latest l JOIN daily d USING (product_id);
