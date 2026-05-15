# Automated Monthly Taxi Data Pipeline

An End-to-End Data Engineering project utilizing **Apache Airflow**, **Python**, and **Docker** to automate the ingestion, transformation, and modeling of NYC Taxi Trip datasets using the **Medallion Architecture**.

## Project Overview

This project builds a robust, idempotent data pipeline that processes massive monthly taxi datasets (2.2M+ rows). It handles the progression of data from raw Parquet files to a clean, partitioned **Star Schema** ready for Business Intelligence tools like Power BI.

## System Architecture

The pipeline follows the **Medallion Architecture** to ensure data quality and reliability:

1. **Bronze Layer (Raw Source):** Automated ingestion from the landing zone to historical storage with state tracking.
2. **Silver Layer (Cleaned & Enriched):** Filters anomalies (negative fares, unrealistic durations) and performs feature engineering.
3. **Gold Layer (Analytical Serving):** Organizes data into Fact and Dimension tables using **Hive-style Partitioning** for optimized query performance.

## Tech Stack

* **Orchestration:** Apache Airflow
* **Processing Engine:** Python (Pandas / PyArrow)
* **Storage Format:** Apache Parquet (Columnar Storage)
* **Environment:** Docker & Docker Compose
* **Data Modeling:** Star Schema & Hive-style Partitioning

## Project Structure

```text
taxi-de-project/
│── dags/
│   └── monthly_taxi_pipeline.py    # Airflow DAG definition
├── data/                           # Data Lakehouse zones
│   ├── raw/                        # Landing zone for new files
│   ├── bronze/                     # Raw historical copies
│   ├── silver/                     # Cleaned & transformed data
│   ├── gold/                       # Partitioned Star Schema
│   └── processed_files.txt         # State ledger for idempotency
├── scripts/                        # Modular processing logic
│   ├── extract_bronze.py           # Ingestion logic
│   ├── transform_silver.py         # DQ & Transformation
│   ├── build_gold.py               # Star Schema modeling
│   ├── test_*.py                   # Modular unit tests
├── docker-compose.yml              # Container orchestration
└── requirements.txt                # Python dependencies

```

## Data Pipeline Stages (DAG)

The Airflow DAG controls the dependency flow using **XComs** to pass file paths dynamically between tasks:

1. **`extract_bronze`**: Scans the `raw/` directory. If a new `.parquet` file is found, it copies it to `bronze/` and logs it in `processed_files.txt`.
2. **`transform_silver`**:
* Ensures `fare_amount >= 0` and `trip_distance > 0`.
* Calculates `trip_duration_minutes`.
* Extracts time-based features (Hour, Day Name, Month).


3. **`build_gold`**:
* Creates a **Fact Table** (`fact_taxi_trips`) partitioned by month.
* Creates a **Dimension Table** (`dim_date`) for time-series analysis.



## How to Run

### 1. Prerequisites

* Docker and Docker Compose installed.
* New York Taxi `.parquet` files placed in `data/raw/`.

### 2. Deployment

```bash
# Build and start the Airflow containers
docker-compose up -d

```

### 3. Execution

1. Access the Airflow Web UI at `http://localhost:8080`.
2. Enable the `monthly_taxi_ingestion` DAG.
3. The pipeline will automatically detect files in `data/raw/` and process them through the layers.

### 4. Testing

You can test individual components inside the container:

```bash
docker exec -it <container_id> python3 scripts/test_extract.py
docker exec -it <container_id> python3 scripts/test_silver.py
docker exec -it <container_id> python3 scripts/test_gold.py

```

## Data Modeling & Optimization

* **Idempotency:** The pipeline uses a state ledger to ensure that re-running the DAG does not ingest the same file twice.
* **Partitioning:** The Gold Layer implements Hive-style partitioning (`month=YYYY-MM`), enabling **Partition Pruning** in query engines to reduce I/O costs and improve speed.

---

**Author:** Natnicha Sohmalee 66102010579
**Project Date:** May 2026
