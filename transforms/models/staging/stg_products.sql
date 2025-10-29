{{
  config(
    materialized='view'
  )
}}

SELECT
  id,
  name,
  brand,
  category,
  description,
  price,
  created_at,
  updated_at
FROM {{ source('dev', 'products') }}