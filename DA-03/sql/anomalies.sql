CREATE OR REPLACE VIEW anomaly_demand AS
WITH mx AS (SELECT MAX(ts) AS m FROM inventory_hourly),
b AS (
    SELECT i.product_id,
           FLOOR(EXTRACT(EPOCH FROM (mx.m - i.ts)) / 86400)::int AS days_ago,
           SUM(i.units_sold) AS units
    FROM inventory_hourly i, mx
    GROUP BY 1, 2
),
base AS (
    SELECT product_id, AVG(units) AS mu, STDDEV(units) AS sd
    FROM b WHERE days_ago >= 2 GROUP BY product_id
)
SELECT b.product_id, b.days_ago, b.units,
       ROUND(base.mu, 1) AS baseline_units,
       ROUND(((b.units - base.mu) / NULLIF(base.sd, 0))::numeric, 2) AS z_score
FROM b JOIN base USING (product_id)
WHERE b.days_ago < 2
  AND (b.units - base.mu) / NULLIF(base.sd, 0) > 3;

CREATE OR REPLACE VIEW anomaly_supplier_delay AS
WITH d AS (
    SELECT supplier_id,
           EXTRACT(EPOCH FROM (delivered_at - promised_at)) / 86400 AS delay
    FROM shipments WHERE delivered_at IS NOT NULL
),
st AS (SELECT AVG(delay) AS mu, STDDEV(delay) AS sd FROM d),
z AS (SELECT supplier_id, delay, (delay - st.mu) / st.sd AS zs FROM d, st)
SELECT supplier_id,
       COUNT(*) AS delayed_shipments,
       ROUND(AVG(delay)::numeric, 2) AS avg_delay_days,
       ROUND(MAX(zs)::numeric, 2) AS max_z_score
FROM z WHERE zs > 3
GROUP BY supplier_id;