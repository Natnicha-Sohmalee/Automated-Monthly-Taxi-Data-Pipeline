# ระบุ path ของ module ให้ชัดเจน
from scripts.extract_bronze import move_new_file_to_bronze

if __name__ == "__main__":
    print("Starting Extraction Test...")
    result = move_new_file_to_bronze()
    print(f"Extraction Test Completed. Result: {result}")