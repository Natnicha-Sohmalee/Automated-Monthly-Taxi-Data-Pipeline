import os
from scripts.build_gold import build_gold

# ใช้ Absolute Path
silver_dir = "/opt/airflow/data/silver"

def run_test():
    if not os.path.exists(silver_dir) or not os.listdir(silver_dir):
        print("No files found in silver directory.")
        return

    # ดึงไฟล์ล่าสุดจาก Silver
    files = [f for f in os.listdir(silver_dir) if f.endswith(".parquet")]
    if not files:
        print("No .parquet files found in silver.")
        return

    latest_file = sorted(files)[-1]
    full_path = os.path.join(silver_dir, latest_file)
    
    print(f"Testing Gold Build with file: {latest_file}")
    build_gold(full_path)

if __name__ == "__main__":
    run_test()