{{
  config(
    materialized='view'
  )
}}

SELECT 
  id,
  salutation,
  first_name,
  last_name,
  email,
  phone,
  created_at,
  updated_at
FROM {{ source('dev', 'customers') }}