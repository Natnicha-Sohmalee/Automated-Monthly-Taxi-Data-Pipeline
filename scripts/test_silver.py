import os
from scripts.transform_silver import clean_data

# ใช้ Absolute Path เพื่อให้หาโฟลเดอร์ data เจอแน่นอน
bronze_dir = "/opt/airflow/data/bronze"

def run_test():
    if not os.path.exists(bronze_dir) or not os.listdir(bronze_dir):
        print("No files found in bronze directory.")
        return

    # ดึงไฟล์ล่าสุดจาก Bronze
    files = [f for f in os.listdir(bronze_dir) if f.endswith(".parquet")]
    if not files:
        print("No .parquet files found in bronze.")
        return
        
    latest_file = sorted(files)[-1]
    full_path = os.path.join(bronze_dir, latest_file)
    
    print(f"Testing Silver Transformation with file: {latest_file}")
    clean_data(full_path)

if __name__ == "__main__":
    run_test()