import subprocess

def run_dbt():
    subprocess.run(
        ["dbt", "run"],
        cwd="opt/airflow/dbt_weather",
        check=True
    )
