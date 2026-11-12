with orders as (
    select * from {{ ref('stg_orders') }}
    where order_status = 'delivered'
),

customers as (
    select * from {{ ref('stg_customers') }}
),

payments as (
    select order_id, sum(payment_value) as order_value
    from {{ ref('stg_payments') }}
    group by order_id
)

select
    c.customer_unique_id,
    count(distinct o.order_id) as frequency,
    sum(p.order_value) as monetary,
    max(o.ordered_at) as last_order_at,
    min(o.ordered_at) as first_order_at
from orders o
join customers c on o.customer_id = c.customer_id
join payments p on o.order_id = p.order_id
group by c.customer_unique_id
