import os
import shutil

BASE_DIR = "/opt/airflow/data"
PROCESSED_FILE = os.path.join(BASE_DIR, "processed_files.txt")
RAW_DIR = os.path.join(BASE_DIR, "raw")
BRONZE_DIR = os.path.join(BASE_DIR, "bronze")

def get_processed():
    if not os.path.exists(PROCESSED_FILE):
        return []
    with open(PROCESSED_FILE, "r") as f:
        return f.read().splitlines()

def mark_processed(file_name):
    os.makedirs(os.path.dirname(PROCESSED_FILE), exist_ok=True)
    with open(PROCESSED_FILE, "a") as f:
        f.write(file_name + "\n")

def move_new_file_to_bronze():
    os.makedirs(BRONZE_DIR, exist_ok=True)
    
    if not os.path.exists(RAW_DIR):
        print(f"Error: Directory {RAW_DIR} not found.")
        return None

    processed = get_processed()
    files = sorted([f for f in os.listdir(RAW_DIR) if f.endswith(".parquet")])

    for file in files:
        if file not in processed:
            source = os.path.join(RAW_DIR, file)
            destination = os.path.join(BRONZE_DIR, file)
            
            shutil.copy(source, destination)
            mark_processed(file)
            print(f"New file ingested: {file}")
            return destination

    print("No new files")
    return None