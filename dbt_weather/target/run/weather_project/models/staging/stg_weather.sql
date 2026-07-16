
  create view "weather_db"."public"."stg_weather__dbt_tmp"
    
    
  as (
    SELECT 
  CAST(time AS TIMESTAMP) AS date, 
  temperature_2m
FROM public.weather
ORDER BY date DESC
  );