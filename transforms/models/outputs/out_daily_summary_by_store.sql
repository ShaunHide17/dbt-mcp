{{
  config(
    materialized='table'
  )
}}

SELECT
  d.date_day as date,
  store_name,
  SUM(amount) as total_amount,
  COUNT(DISTINCT customer_id) as total_customers,
  COUNT(DISTINCT product_id) as total_products
FROM {{ ref('int_transactions') }} t
INNER JOIN {{ ref('int_dates') }} d
  ON t.transaction_date = d.date_day
GROUP BY t.store_name, d.date_day
ORDER BY t.store_name, d.date_day DESC