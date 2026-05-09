import duckdb
import pandas as pd

con = duckdb.connect("weather.db")
result = con.execute(""" SELECT * 
                FROM weather
                ORDER BY date DESC
                limit 10
            """).fetchall()

print(result)
