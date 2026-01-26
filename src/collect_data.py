import os
import requests
from ultralytics.utils import LOGGER
import time

def download_images(query, num_images=50, output_dir='data/raw'):
    """
    Simulated image downloader using placeholders.
    In a real scenario, we would use 'duckduckgo_search' or Bing API.
    Since we cannot easily install complex scrapers without potential bans, 
    this script sets up the folder structure and guides the user.
    """
    
    # Create directory
    target_folder = os.path.join(output_dir, query.replace(" ", "_"))
    os.makedirs(target_folder, exist_ok=True)
    
    print(f"--- Đang chuẩn bị tải ảnh cho từ khóa: '{query}' ---")
    print(f"Lưu tại: {target_folder}")
    
    # Instructions for User (Since automated scraping is often blocked or requires API keys)
    print("\nLƯU Ý QUAN TRỌNG:")
    print("Để có bộ dữ liệu tốt nhất cho xe Việt Nam, cách hiệu quả nhất là:")
    print(10 * "-")
    print(f"1. Vào Google Images/Youtube tìm: '{query}'")
    print(f"2. Tải các ảnh rõ nét về.")
    print(f"3. Copy ảnh vào thư mục: {os.path.abspath(target_folder)}")
    print(10 * "-")
    
    # Creating a dummy file just to show structure works
    with open(os.path.join(target_folder, "readme.txt"), "w", encoding="utf-8") as f:
        f.write(f"Hãy bỏ ảnh {query} vào đây để tiến hành training.")
        
    print(f"Đã tạo xong thư mục chứa ảnh cho '{query}'.")

if __name__ == "__main__":
    classes = [
        "xe cuu thuong vietnam",
        "xe canh sat giao thong vietnam",
        "xe cuu hoa vietnam",
        "xe quan doi vietnam"
    ]
    
    print("Bắt đầu khởi tạo bộ dữ liệu...")
    for c in classes:
        download_images(c)
    
    print("\nHoàn tất khởi tạo cấu trúc folder.")
