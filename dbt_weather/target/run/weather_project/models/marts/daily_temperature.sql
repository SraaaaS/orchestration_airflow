
  
    

  create  table "weather_db"."public"."daily_temperature__dbt_tmp"
  
  
    as
  
  (
    SELECT 
    date::DATE as date, 
    ROUND(CAST(AVG(temperature_2m) AS NUMERIC),2) AS t_journaliere
FROM "weather_db"."public"."stg_weather"
GROUP BY 1
ORDER BY date DESC
  );
  