{{
  config(
    materialized='view'
  )
}}

SELECT 

  t.id,
  t.customer_id,
  c.first_name || ' ' || c.last_name AS customer_name,
  t.product_id,
  p.name AS product_name,
  t.store_id,
  s.name AS store_name,
  t.transaction_date,
  t.amount,
  t.currency,
  t.payment_method,
  t.payment_status,
  t.payment_reference

FROM {{ ref('stg_transactions') }} t
INNER JOIN {{ ref('stg_customers') }} c
  ON t.customer_id = c.id
INNER JOIN {{ ref('stg_products') }} p
  ON t.product_id = p.id
INNER JOIN {{ ref('stg_stores') }} s
  ON t.store_id = s.id