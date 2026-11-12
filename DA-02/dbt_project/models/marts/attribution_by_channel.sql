with t as (
    select
        *,
        timestamp_diff(
            max(session_start) over (partition by order_id),
            session_start,
            hour
        ) / 24.0 as days_before
    from {{ ref('touchpoints') }}
),

weighted as (
    select
        *,
        pow(0.5, days_before / 7) as weight,
        sum(pow(0.5, days_before / 7)) over (partition by order_id) as weight_total
    from t
)

select
    channel,
    round(sum(case when touch_num = 1 then order_value else 0 end), 2) as first_touch_revenue,
    round(sum(case when touch_num = touch_total then order_value else 0 end), 2) as last_touch_revenue,
    round(sum(order_value / touch_total), 2) as linear_revenue,
    round(sum(order_value * weight / weight_total), 2) as time_decay_revenue
from weighted
group by channel
order by channel
