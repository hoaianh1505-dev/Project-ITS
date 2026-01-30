from ultralytics import YOLO
import os
import cv2

# Mapping folder names to Class IDs for our custom model
# 0: cuu thuong, 1: canh sat, 2: cuu hoa, 3: quan doi
# (Adjust indices as per your preference, but consisteny is key)
CLASS_MAPPING = {
    "xe_cuu_thuong_vietnam": 0, # Ambulance
    "xe_canh_sat_giao_thong_vietnam": 1, # Police
    "xe_cuu_hoa_vietnam": 2,    # Fire Truck
    "xe_quan_doi_vietnam": 3    # Army
}
# Standard YOLO COCO classes that represent "vehicles"
# We will use these to find "where the car is", then relabel it.
# 2: Car, 3: Motorcycle, 5: Bus, 7: Truck
VEHICLE_CLASSES = [2, 3, 5, 7]

def auto_label():
    model = YOLO('yolov8n.pt')
    raw_dir = 'data/raw'
    
    print("--- BẮT ĐẦU TỰ ĐỘNG DÁN NHÃN ---")
    
    total_labeled = 0
    
    # Iterate through each category folder
    for folder_name, target_class_id in CLASS_MAPPING.items():
        folder_path = os.path.join(raw_dir, folder_name)
        if not os.path.exists(folder_path):
            print(f"Bỏ qua: Không thấy thư mục {folder_name}")
            continue
            
        print(f"Đang xử lý thư mục: {folder_name} (Class ID: {target_class_id})...")
        
        images = [f for f in os.listdir(folder_path) if f.lower().endswith(('.jpg', '.png', '.jpeg'))]
        
        for img_file in images:
            img_path = os.path.join(folder_path, img_file)
            
            # Run detection using base model
            results = model(img_path, verbose=False)[0]
            
            # Find the "Best" vehicle in the image (Largest area)
            # Assumption: The training image mostly focuses on the subject vehicle.
            best_box = None
            max_area = 0
            
            for box in results.boxes:
                cls_id = int(box.cls[0])
                if cls_id in VEHICLE_CLASSES:
                    # Calculate area
                    xywh = box.xywh[0] # x, y, width, height
                    area = float(xywh[2] * xywh[3])
                    
                    if area > max_area:
                        max_area = area
                        best_box = box
            
            # If we found a vehicle, save label
            txt_path = os.path.join(folder_path, os.path.splitext(img_file)[0] + ".txt")
            
            if best_box is not None:
                # YOLO format: class_id x_center y_center width height (normalized)
                xywhn = best_box.xywhn[0]
                line = f"{target_class_id} {xywhn[0]:.6f} {xywhn[1]:.6f} {xywhn[2]:.6f} {xywhn[3]:.6f}\n"
                
                with open(txt_path, "w") as f:
                    f.write(line)
                
                total_labeled += 1
            else:
                # No vehicle found? Maybe manual fallback or skip
                print(f"  Cảnh báo: Không tìm thấy xe trong ảnh {img_file}")

    print(f"--- HOÀN TẤT: Đã dán nhãn tự động cho {total_labeled} ảnh ---")
    print("Bạn có thể chạy 'src/split_data.py' ngay bây giờ.")

if __name__ == '__main__':
    auto_label()
