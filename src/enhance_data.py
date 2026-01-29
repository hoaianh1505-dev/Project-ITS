import cv2
import os
import numpy as np
import shutil
import random

def enhance_data():
    RAW_DIR = 'data/raw'
    NEW_DIR = 'data/raw_enhanced'
    CANVAS_SIZE = 640
    
    # Target size for the vehicle: random between 200 (30%) and 350 (55%) of canvas
    MIN_OBJ_SIZE = 200
    MAX_OBJ_SIZE = 350

    print(f"--- BẮT ĐẦU XỬ LÝ ẢNH (Zoom Out Effect) ---")
    
    if os.path.exists(NEW_DIR):
        shutil.rmtree(NEW_DIR)
    os.makedirs(NEW_DIR)

    categories = [d for d in os.listdir(RAW_DIR) if os.path.isdir(os.path.join(RAW_DIR, d))]
    
    total_processed = 0

    for category in categories:
        src_folder = os.path.join(RAW_DIR, category)
        dst_folder = os.path.join(NEW_DIR, category)
        os.makedirs(dst_folder, exist_ok=True)
        
        images = [f for f in os.listdir(src_folder) if f.strip().lower().endswith(('.jpg', '.jpeg', '.png', '.bmp'))]
        
        print(f"-> Đang xử lý: {category} ({len(images)} ảnh)")
        
        for img_name in images:
            img_path = os.path.join(src_folder, img_name)
            img = cv2.imread(img_path)
            
            if img is None:
                continue
                
            h, w = img.shape[:2]
            
            # Create black canvas
            canvas = np.zeros((CANVAS_SIZE, CANVAS_SIZE, 3), dtype=np.uint8)
            
            # Determine new scale
            target_size = random.randint(MIN_OBJ_SIZE, MAX_OBJ_SIZE)
            scale = target_size / max(h, w)
            
            new_w = int(w * scale)
            new_h = int(h * scale)
            
            resized_img = cv2.resize(img, (new_w, new_h), interpolation=cv2.INTER_AREA)
            
            # Calculate center position with slight random jitter
            center_x = CANVAS_SIZE // 2
            center_y = CANVAS_SIZE // 2
            
            offset_x = random.randint(-50, 50)
            offset_y = random.randint(-50, 50)
            
            start_x = center_x - new_w // 2 + offset_x
            start_y = center_y - new_h // 2 + offset_y
            
            # Ensure within bounds
            start_x = max(0, min(start_x, CANVAS_SIZE - new_w))
            start_y = max(0, min(start_y, CANVAS_SIZE - new_h))
            
            # Paste image
            canvas[start_y:start_y+new_h, start_x:start_x+new_w] = resized_img
            
            # Save
            save_path = os.path.join(dst_folder, img_name)
            cv2.imwrite(save_path, canvas)
            total_processed += 1
            
    print(f"--- HOÀN TẤT: Đã xử lý {total_processed} ảnh ---")
    print(f"Ảnh mới được lưu tại: {NEW_DIR}")

if __name__ == "__main__":
    enhance_data()
