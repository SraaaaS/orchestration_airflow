FROM apache/airflow:2.9.1

WORKDIR /opt/airflow

COPY requirements.txt . 

USER airflow
COPY dags/ /opt/airflow/dags
COPY scripts/ /opt/airflow/scripts
COPY data/ /opt/airflow/data

RUN pip install --no-cache-dir -r requirements.txt
