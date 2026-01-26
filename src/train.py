from ultralytics import YOLO
import os

def train_model():
    # 1. Load the model
    # We start from 'yolov8n.pt' (pretrained) to fine-tune
    model = YOLO('yolov8n.pt') 

    # 2. Train the model
    # data='data.yaml' -> We need to generate this file dynamically or ask user to create it
    # epochs=50 -> Number of times to iterate over data
    # imgsz=640 -> Image size
    
    yaml_path = os.path.abspath('data.yaml')
    
    print(f"Bắt đầu training với cấu hình tại: {yaml_path}")
    
    results = model.train(
        data=yaml_path,
        epochs=50,
        imgsz=640,
        device='cpu', # Or '0' for GPU if available
        plots=True
    )
    
    print("Training hoàn tất!")
    print(f"Model mới được lưu tại: {results.save_dir}")
    print("Hãy copy file 'best.pt' trong đó ra ngoài để chạy App.")

if __name__ == '__main__':
    # Check if data.yaml exists
    if not os.path.exists('data.yaml'):
        print("LỖI: Chưa thấy file 'data.yaml'.")
        print("Bạn cần chạy script 'src/split_data.py' trước để tạo dữ liệu và file cấu hình.")
    else:
        train_model()
