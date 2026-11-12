select
    s.session_id,
    s.channel,
    s.session_start,
    s.converted_order_id as order_id_conv,
    o.order_id,
    p.order_value,
    row_number() over (partition by o.order_id order by s.session_start) as touch_num,
    count(*) over (partition by o.order_id) as touch_total
from {{ ref('stg_sessions') }} s
join {{ ref('stg_customers') }} c on s.customer_unique_id = c.customer_unique_id
join {{ ref('stg_orders') }} o on o.customer_id = c.customer_id
join (
    select order_id, sum(payment_value) as order_value
    from {{ ref('stg_payments') }}
    group by order_id
) p on p.order_id = o.order_id
where s.converted_order_id = o.order_id
   or s.session_start < o.ordered_at
