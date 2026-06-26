SELECT 
    date, 
    ROUND(CAST(AVG(temperature_2m) AS NUMERIC),2) AS t_journaliere
FROM {{ ref('stg_weather') }}
GROUP BY 1
