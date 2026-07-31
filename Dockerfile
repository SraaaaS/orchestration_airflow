FROM apache/airflow:2.9.1

WORKDIR /opt/airflow

COPY requirements.txt . 

USER root

COPY dags/ /opt/airflow/dags
COPY scripts/ /opt/airflow/scripts
COPY dbt_weather /opt/airflow/dbt_weather
COPY data/ /opt/airflow/data

USER airflow

RUN pip install --no-cache-dir --upgrade pip
RUN pip install -vvv --no-cache-dir -r requirements.txt
RUN pip install --no-cache-dir psycopg2-binary
RUN pip install --no-cache-dir dbt-postgres==1.8.2
