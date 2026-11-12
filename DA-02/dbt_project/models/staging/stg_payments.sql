select
    order_id,
    payment_type,
    payment_value
from {{ source('capstone', 'payments') }}
