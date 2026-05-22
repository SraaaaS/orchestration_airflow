# Pipeline ETL Météo avec Airflow, Docker et DuckDB

## Présentation du projet

Ce projet est une pipeline ETL (Extract, Transform, Load) de bout en bout développée avec :

* Apache Airflow
* Docker & Docker Compose
* Python
* DuckDB
* Pandas
* API Open-Meteo

L’objectif du projet est d’automatiser la récupération, la transformation et le stockage de données météorologiques historiques à travers une architecture proche des environnements utilisés en entreprise.

La pipeline :

* récupère automatiquement les données météo historiques,
* transforme les données horaires en indicateurs journaliers,
* stocke les résultats dans une base DuckDB,
* orchestre toutes les étapes via Airflow,
* s’exécute automatiquement selon une planification définie.

Ce projet simule un workflow réel de Data Engineering avec :

* orchestration de tâches,
* automatisation,
* chargement incrémental,
* gestion des dépendances,
* conteneurisation,
* monitoring via Airflow.

---

# Architecture du projet

```text
                +-------------------+
                | API Open-Meteo    |
                +---------+---------+
                          |
                          v
                +-------------------+
                | Tâche Extract     |
                | raw_weather.csv   |
                +---------+---------+
                          |
                          v
                +-------------------+
                | Tâche Transform   |
                | daily_weather.csv |
                +---------+---------+
                          |
                          v
                +-------------------+
                | Tâche Load        |
                | Base DuckDB       |
                +---------+---------+
                          |
                          v
                +-------------------+
                | Tâche Check Data  |
                +-------------------+
```

---

# Technologies utilisées

| Technologie    | Rôle                            |
| -------------- | ------------------------------- |
| Python         | Développement de la logique ETL |
| Apache Airflow | Orchestration des workflows     |
| Docker         | Conteneurisation                |
| Docker Compose | Gestion multi-conteneurs        |
| DuckDB         | Base de données analytique      |
| Pandas         | Transformation des données      |
| API Open-Meteo | Source des données météo        |
| PostgreSQL     | Base de métadonnées Airflow     |

---

# Structure du projet

```text
weather-etl-project/
│
├── dags/
│   └── etl_dag.py
│
├── scripts/
│   ├── extract.py
│   ├── transform.py
│   ├── load.py
│   └── check_data.py
│
├── data/
│   ├── raw_weather_data.csv
│   ├── daily_weather_data.csv
│   └── weather.db
│
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
└── README.md
```

---

# Fonctionnement de la pipeline

## 1. Extract

L’étape d’extraction :

* interroge l’API Open-Meteo,
* récupère les températures horaires historiques,
* supprime les timestamps futurs,
* ajoute uniquement les nouvelles données,
* stocke les données brutes dans :

```text
/opt/airflow/data/raw_weather_data.csv
```

### Fonctionnalités

* ingestion incrémentale,
* prévention des doublons,
* gestion des timestamps UTC,
* mise à jour automatique des données historiques.

---

## 2. Transform

L’étape de transformation :

* convertit les timestamps en datetime,
* groupe les données par jour,
* calcule les températures moyennes journalières,
* arrondit les valeurs à deux décimales,
* sauvegarde les données transformées dans :

```text
/opt/airflow/data/daily_weather_data.csv
```

Exemple de résultat :

| date       | T_moyenne |
| ---------- | --------- |
| 2026-05-19 | 16.95     |
| 2026-05-20 | 17.12     |

---

## 3. Load

L’étape de chargement :

* se connecte à DuckDB,
* crée la table weather si elle n’existe pas,
* insère uniquement les nouvelles lignes,
* évite d’écraser l’historique précédent.

Chemin de la base :

```text
/opt/airflow/data/weather.db
```

Schéma SQL :

```sql
CREATE TABLE weather (
    date DATE,
    T_moyenne DECIMAL(5,2)
)
```

---

## 4. Check Data

La dernière tâche :

* interroge la base DuckDB,
* vérifie les lignes insérées,
* contrôle que le chargement s’est correctement effectué.

---

# DAG Airflow

Le DAG orchestre toutes les tâches ETL :

```text
extract >> transform >> load >> check_data
```

### Fonctionnalités du DAG

* exécution planifiée toutes les heures,
* gestion automatique des retries,
* monitoring des tâches,
* gestion des dépendances,
* centralisation des logs.

Exemple :

```python
schedule_interval = "@hourly"
```

---

# Mise en place avec Docker

Le projet fonctionne entièrement dans des conteneurs Docker.

Services utilisés :

* airflow-webserver
* airflow-scheduler
* airflow-init
* postgres

Avantages :

* environnement reproductible,
* isolation des dépendances,
* architecture proche de la production,
* déploiement simplifié.

---

# Dockerfile

L’image Docker personnalisée :

* étend l’image officielle Airflow,
* installe les dépendances du projet,
* copie les DAGs et scripts,
* standardise l’environnement d’exécution.

Exemple :

```dockerfile
FROM apache/airflow:2.9.1

USER airflow

WORKDIR /opt/airflow

COPY requirements.txt .
COPY dags/ /opt/airflow/dags
COPY scripts/ /opt/airflow/scripts
COPY data/ /opt/airflow/data

RUN pip install --no-cache-dir -r requirements.txt
```

---

# Exécution du projet

## 1. Initialiser Airflow

```bash
docker-compose up airflow-init
```

---

## 2. Construire le conteneur et lancer les services

```bash
docker-compose up --build
```

---

## 3. Accéder à l’interface Airflow

```text
http://localhost:8080
```

Identifiants par défaut :

```text
Username: airflow
Password: airflow
```

---

# Chargement incrémental

Une amélioration importante du projet a consisté à implémenter un chargement incrémental.

Au lieu de :

* supprimer la table,
* recharger tout l’historique,

la pipeline :

* ajoute uniquement les nouvelles lignes,
* évite les doublons,
* conserve l’historique précédent.

Cette approche se rapproche des pipelines ETL modernes utilisés en entreprise.

---

# Difficultés rencontrées

Durant le développement, plusieurs problématiques proches des environnements réels ont été résolues :

* incohérences de chemins Docker,
* création accidentelle de plusieurs bases DuckDB,
* conflits de types entre VARCHAR et DATE,
* verrouillage concurrent de DuckDB,
* problèmes de configuration Airflow,
* logique d’actualisation incrémentale,
* gestion des timestamps futurs,
* permissions Docker et gestion des utilisateurs Airflow.

---

# Compétences démontrées

Ce projet met en avant des compétences en :

* Data Engineering,
* développement ETL,
* orchestration de workflows,
* Docker,
* Airflow,
* SQL et DuckDB,
* traitement de données avec Python,
* pipelines incrémentales,
* debugging de systèmes distribués,
* architecture orientée production.

---

# Améliorations possibles

Pistes d’évolution du projet :

* ajout d’un dashboard de visualisation,
* migration vers PostgreSQL,
* déploiement cloud,
* mise en place de CI/CD,
* ajout de tests unitaires,
* validation de qualité des données,
* stockage en format Parquet,
* monitoring et alerting,
* détection d’anomalies météo.

---

# Ce que ce projet a permis d’apprendre

Ce projet a permis de développer une compréhension concrète :

* du fonctionnement d’Airflow,
* de l’orchestration de pipelines,
* des interactions entre conteneurs Docker,
* de la persistance des volumes,
* des pipelines ETL de production,
* de la planification automatique,
* de la gestion des erreurs et retries,
* du debugging de systèmes orchestrés.

---

# Auteur

Projet réalisé dans le cadre d’un apprentissage pratique du Data Engineering et de l’orchestration de pipelines ETL dans un environnement conteneurisé proche de la production.
