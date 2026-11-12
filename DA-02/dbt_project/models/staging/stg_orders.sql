select
    order_id,
    customer_id,
    order_status,
    cast(order_purchase_timestamp as timestamp) as ordered_at
from {{ source('capstone', 'orders') }}
