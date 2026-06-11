SELECT 
    date, 
    ROUND(AVG(temperature_2m),2) AS t_journaliere
FROM "weather"."main"."stg_weather"
GROUP BY 1