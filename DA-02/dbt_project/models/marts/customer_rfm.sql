with base as (
    select
        customer_unique_id,
        date_diff(
            (select date(max(last_order_at)) from {{ ref('customer_profile') }}),
            date(last_order_at),
            day
        ) as recency_days,
        frequency,
        monetary
    from {{ ref('customer_profile') }}
),

scored as (
    select
        *,
        ntile(5) over (order by recency_days desc) as r_score,
        ntile(5) over (order by frequency) as f_score,
        ntile(5) over (order by monetary) as m_score
    from base
)

select
    *,
    case
        when r_score >= 4 and m_score >= 4 then 'Champions'
        when r_score >= 3 and m_score >= 3 then 'Loyal'
        when r_score >= 4 then 'New Customers'
        when r_score <= 2 and m_score >= 4 then 'At Risk'
        when r_score <= 2 then 'Lost'
        else 'Potential'
    end as segment
from scored
