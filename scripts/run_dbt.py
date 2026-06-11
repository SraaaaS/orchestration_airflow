import subprocess
import os

def run_dbt():
    # On utilise le chemin absolu trouvé avec ton "which dbt"
    dbt_path = "/home/airflow/.local/bin/dbt"
    
    # On s'assure que l'environnement contient le PATH
    env = os.environ.copy()

    result = subprocess.run(
        [dbt_path, "run", "--project-dir", "/opt/airflow/dbt_weather", "--profiles-dir", "/opt/airflow/dbt_weather", "--full-refresh"],
        capture_output=True,
        text=True,
        env=env
    )

    print("STDOUT:\n", result.stdout)
    print("STDERR:\n", result.stderr)

    result.check_returncode()