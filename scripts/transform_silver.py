import pandas as pd
import os

def clean_data(bronze_path):
    # ปรับ Path ให้เป็น Absolute สำหรับการทำงานบน Docker
    BASE_DIR = "/opt/airflow/data"
    silver_dir = os.path.join(BASE_DIR, "silver")
    
    # อ่านข้อมูลจาก Bronze
    df = pd.read_parquet(bronze_path)

    print("Rows Before:", len(df))

    # Data Quality
    df = df[df["fare_amount"] >= 0]
    df = df[df["trip_distance"] > 0]
    df = df[df["passenger_count"] > 0]

    df = df.dropna(subset=["tpep_pickup_datetime", "tpep_dropoff_datetime"])

    # Datetime transformation
    df["pickup_time"] = pd.to_datetime(df["tpep_pickup_datetime"])
    df["dropoff_time"] = pd.to_datetime(df["tpep_dropoff_datetime"])

    # Trip duration calculations
    df["trip_duration_minutes"] = (df["dropoff_time"] - df["pickup_time"]).dt.total_seconds() / 60

    # Time features
    df["pickup_hour"] = df["pickup_time"].dt.hour
    df["pickup_day_name"] = df["pickup_time"].dt.day_name()
    df["pickup_month"] = df["pickup_time"].dt.month

    # Remove anomalies
    df = df[(df["trip_duration_minutes"] > 0) & (df["trip_duration_minutes"] < 1440)]

    # สร้างโฟลเดอร์ Silver หากยังไม่มี
    os.makedirs(silver_dir, exist_ok=True)

    # จัดการชื่อไฟล์เพื่อระบุเดือน
    file_name = os.path.basename(bronze_path)
    # สมมติชื่อไฟล์ต้นฉบับคือ yellow_tripdata_2024-01.parquet
    month_tag = file_name.replace("yellow_tripdata_", "").replace(".parquet", "")

    output_path = os.path.join(
        silver_dir, 
        f"clean_taxi_data_{month_tag}.parquet"
    )

    # บันทึกไฟล์
    df.to_parquet(output_path)

    print("Rows After:", len(df))
    print("Saved Silver Layer:", output_path)

    return output_path