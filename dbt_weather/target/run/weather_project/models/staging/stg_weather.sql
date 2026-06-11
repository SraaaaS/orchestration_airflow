
  
  create view "weather"."main"."stg_weather__dbt_tmp" as (
    SELECT 
  CAST(time AS TIMESTAMP) AS date, 
  temperature_2m
FROM weather
  );
