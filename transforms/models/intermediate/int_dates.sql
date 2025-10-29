{{
  config(
    materialized='table'
  )
}}

WITH 
  dates as (
    SELECT generate_series(
    date_trunc('day', current_date) - interval '1 years',
    date_trunc('day', current_date),
    interval '1 day'
  ) as date_day
)
SELECT
  date_day,
  date_trunc('month', date_day) as date_month,
  date_trunc('year', date_day) as date_year,
  date_part('dow', date_day) as date_day_of_week,
  date_part('day', date_day) as date_day_of_month,
  date_part('doy', date_day) as date_day_of_year
FROM dates
