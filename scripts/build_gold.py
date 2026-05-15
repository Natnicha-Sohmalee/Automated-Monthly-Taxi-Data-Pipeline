import pandas as pd
import os

def build_gold(silver_path):
    # 1. กำหนดโครงสร้าง Path พื้นฐาน (Absolute Path สำหรับ Docker)
    BASE_DIR = "/opt/airflow/data"
    gold_dir = os.path.join(BASE_DIR, "gold")

    # 2. อ่านข้อมูลจาก Silver Layer
    if not os.path.exists(silver_path):
        print(f"Error: Silver file not found at {silver_path}")
        return None
        
    df = pd.read_parquet(silver_path)

    # 3. สร้าง Fact Table (ข้อมูลธุรกรรมหลัก)
    fact = pd.DataFrame()
    fact["pickup_datetime"] = df["pickup_time"]
    fact["pickup_location_id"] = df["PULocationID"]
    fact["dropoff_location_id"] = df["DOLocationID"]
    fact["fare_amount"] = df["fare_amount"]
    fact["tip_amount"] = df["tip_amount"]
    fact["total_amount"] = df["total_amount"]
    fact["trip_distance"] = df["trip_distance"]
    fact["trip_duration_minutes"] = df["trip_duration_minutes"]

    # 4. สร้าง Date Dimension (ข้อมูลมิติวันที่)
    dim_date = pd.DataFrame()
    dim_date["date"] = pd.to_datetime(df["pickup_time"]).dt.date
    dim_date = dim_date.drop_duplicates()

    dim_date["year"] = pd.to_datetime(dim_date["date"]).dt.year
    dim_date["month"] = pd.to_datetime(dim_date["date"]).dt.month
    dim_date["day_name"] = pd.to_datetime(dim_date["date"]).dt.day_name()

    # 5. จัดการเรื่องชื่อไฟล์และ Tag ประจำเดือน
    file_name = os.path.basename(silver_path)
    # ตัดชื่อไฟล์ให้เหลือแค่ปี-เดือน เช่น "2024-05"
    month_tag = file_name.replace("clean_taxi_data_", "").replace(".parquet", "")

    # 6. บันทึก Dimension Table (เซฟเป็นไฟล์ปกติในโฟลเดอร์ gold)
    os.makedirs(gold_dir, exist_ok=True)
    dim_path = os.path.join(gold_dir, f"dim_date_{month_tag}.parquet")
    dim_date.to_parquet(dim_path)

    # 7. บันทึก Fact Table แบบ Partitioning (Hive-style)
    # สร้างโครงสร้าง: data/gold/fact_taxi_trips/month=2024-05/data.parquet
    partition_dir = os.path.join(
        gold_dir,
        "fact_taxi_trips",
        f"month={month_tag}"
    )
    
    os.makedirs(partition_dir, exist_ok=True)
    fact_path = os.path.join(partition_dir, "data.parquet")
    
    fact.to_parquet(fact_path)

    # 8. แสดงผลลัพธ์การทำงาน
    print(f"--- Gold Layer Process Completed ---")
    print(f"Month Tag: {month_tag}")
    print(f"Dimension Saved: {dim_path}")
    print(f"Fact Partitioned Saved: {fact_path}")
    
    return gold_dir