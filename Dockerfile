FROM apache/airflow:2.9.1

WORKDIR /opt/airflow

COPY requirements.txt . 

USER airflow
COPY dags/ /opt/airflow/dags
COPY scripts/ /opt/airflow/scripts
COPY dbt_weather /opt/airflow/dbt_weather
COPY data/ /opt/airflow/data

RUN pip install --upgrade pip
RUN pip install -vvv --no-cache-dir -r requirements.txt
