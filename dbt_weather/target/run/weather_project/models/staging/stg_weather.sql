
  
  create view "weather"."main"."stg_weather__dbt_tmp" as (
    SELECT 
  CAST(time AS TIMESTAMP) AS time, temperature_2m
FROM weather
  );
