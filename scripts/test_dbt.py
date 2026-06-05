import subprocess

def test_dbt():
  subprocess.run(
    ["dbt", "test"],
    cwd="/opt/airflow/dbt_weather",
    check=True
  )
