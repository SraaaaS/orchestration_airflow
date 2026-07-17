SELECT 
  CAST(time AS TIMESTAMP) AS date, 
  temperature_2m
FROM public.weather
ORDER BY date DESC