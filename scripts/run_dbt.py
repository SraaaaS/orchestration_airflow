import subprocess

def run_dbt():
    
    result = subprocess.run(
    ["dbt", "run", "--project-dir", "/opt/airflow/dbt_weather", "--profiles-dir", "/opt/airflow/dbt_weather"],
    capture_output=True,
    text=True
    )

    print(result.stdout)
    print(result.stderr)

    if result.returncode != 0:
        raise Exception("dbt failed")