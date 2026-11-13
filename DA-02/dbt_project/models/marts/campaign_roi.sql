with spend as (
    select channel, sum(spend) as total_spend
    from {{ source('capstone', 'ad_spend') }}
    group by channel
),

conversions as (
    select channel, count(distinct order_id) as orders
    from {{ ref('touchpoints') }}
    where touch_num = touch_total
    group by channel
)

select
    a.channel,
    round(s.total_spend, 2) as total_spend,
    c.orders as conversions,
    a.last_touch_revenue,
    a.time_decay_revenue,
    round(s.total_spend / nullif(c.orders, 0), 2) as cpa,
    round((a.time_decay_revenue - s.total_spend) / nullif(s.total_spend, 0), 2) as roi
from {{ ref('attribution_by_channel') }} a
join spend s on a.channel = s.channel
left join conversions c on a.channel = c.channel
order by roi desc
