select
    session_id,
    customer_unique_id,
    cast(session_start as timestamp) as session_start,
    channel,
    converted_order_id
from {{ source('capstone', 'session') }}
