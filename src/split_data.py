import os
import shutil
import random
import yaml

# Configuration
RAW_DIR = 'data/raw'
OUTPUT_DIR = 'data'
TRAIN_RATIO = 0.8
SEED = 42
CLASSES = [
    "xe cuu thuong vietnam",
    "xe canh sat giao thong vietnam",
    "xe cuu hoa vietnam",
    "xe quan doi vietnam"
]

def create_yolo_structure():
    # Create standard YOLO folders
    for split in ['train', 'val']:
        for kind in ['images', 'labels']:
            path = os.path.join(OUTPUT_DIR, split, kind)
            os.makedirs(path, exist_ok=True)
            
def process_data():
    create_yolo_structure()
    
    # Iterate over class folders in raw
    # Assumption: User puts images AND .txt labels (YOLO format) in data/raw/<class_name>
    # Note: LabelImg usually saves in the same folder.
    
    all_files = []
    
    # We will treat all classes as one big dataset for now, 
    # but we need to ensure the class IDs in .txt files match our CLASSES list index.
    # This is tricky if user labeled manually. 
    # For now, let's assume user labeled correctly using a classes.txt defined as above.
    
    for class_name in os.listdir(RAW_DIR):
        class_dir = os.path.join(RAW_DIR, class_name)
        if not os.path.isdir(class_dir):
            continue
            
        # Get all image files
        images = [f for f in os.listdir(class_dir) if f.lower().endswith(('.jpg', '.jpeg', '.png'))]
        
        for img_name in images:
            base_name = os.path.splitext(img_name)[0]
            label_name = base_name + '.txt'
            
            img_path = os.path.join(class_dir, img_name)
            label_path = os.path.join(class_dir, label_name)
            
            if os.path.exists(label_path):
                all_files.append((img_path, label_path))
    
    # Shuffle and Split
    # Make shuffle reproducible
    random.seed(SEED)
    random.shuffle(all_files)
    split_index = int(len(all_files) * TRAIN_RATIO)
    train_files = all_files[:split_index]
    val_files = all_files[split_index:]
    
    print(f"Tìm thấy {len(all_files)} cặp ảnh/nhãn hợp lệ.")
    print(f"Train: {len(train_files)} | Val: {len(val_files)}")
    
    def copy_files(files, split):
        for img_src, label_src in files:
            shutil.copy(img_src, os.path.join(OUTPUT_DIR, split, 'images'))
            shutil.copy(label_src, os.path.join(OUTPUT_DIR, split, 'labels'))
            
    copy_files(train_files, 'train')
    copy_files(val_files, 'val')
    
    # Create data.yaml
    data_yaml = {
        'path': os.path.abspath(OUTPUT_DIR),
        'train': 'train/images',
        'val': 'val/images',
        'names': {i: name for i, name in enumerate(CLASSES)}
    }
    
    with open('data.yaml', 'w') as f:
        yaml.dump(data_yaml, f)
    
    print("Đã tạo xong dữ liệu và file 'data.yaml'.")
    print("Sẵn sàng để chạy 'src/train.py'.")

if __name__ == '__main__':
    process_data()
