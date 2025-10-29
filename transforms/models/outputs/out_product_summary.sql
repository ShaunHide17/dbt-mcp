{{
  config(
    materialized='table'
  )
}}

SELECT
  product_name,
  SUM(amount) as total_amount
FROM {{ ref('int_transactions') }}
GROUP BY product_name
ORDER BY total_amount DESC