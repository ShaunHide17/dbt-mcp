{{
  config(
    materialized='view'
  )
}}

SELECT
  id,
  customer_id,
  product_id,
  store_id,
  transaction_date,
  amount,
  currency,
  payment_method,
  payment_status,
  payment_reference
FROM {{ source('dev', 'transactions') }}