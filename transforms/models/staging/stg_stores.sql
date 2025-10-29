{{
  config(
    materialized='view'
  )
}}

SELECT
  id,
  name,
  address,
  city,
  postcode,
  country,
  created_at,
  updated_at
FROM {{ source('dev', 'stores') }}