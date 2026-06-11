SELECT 
    date, 
    ROUND(AVG(temperature_2m),2) AS t_journaliere
FROM {{ ref('stg_weather') }}
GROUP BY 1
