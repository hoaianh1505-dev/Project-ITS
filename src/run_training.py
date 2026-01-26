import os
import shutil
import glob

def run_step(command, step_name):
    print(f"\n{'='*10} BƯỚC: {step_name} {'='*10}")
    ret = os.system(command)
    if ret != 0:
        print(f"LỖI: Bước {step_name} gặp sự cố. Dừng quy trình.")
        exit(1)

def main():
    # 1. Auto Label
    run_step("python src/auto_label.py", "TỰ ĐỘNG DÁN NHÃN")
    
    # 2. Split Data
    run_step("python src/split_data.py", "CHUẨN BỊ DỮ LIỆU")
    
    # 3. Train
    # This takes the longest time
    run_step("python src/train.py", "HUẤN LUYỆN (Training)")
    
    # 4. Copy Model
    print(f"\n{'='*10} BƯỚC: HOÀN TẤT & CẬP NHẬT MODEL {'='*10}")
    # Find the latest training run
    # Ultralytics saves to runs/detect/train, train2, train3...
    runs_dir = "runs/detect"
    if os.path.exists(runs_dir):
        # Get list of train folders
        train_dirs = glob.glob(os.path.join(runs_dir, "train*"))
        if train_dirs:
            # Sort by creation time to get latest
            latest_run = max(train_dirs, key=os.path.getctime)
            best_model_path = os.path.join(latest_run, "weights", "best.pt")
            
            if os.path.exists(best_model_path):
                target_path = "best_model.pt"
                shutil.copy(best_model_path, target_path)
                print(f"Đã copy model mới ra ngoài thành công: {target_path}")
                print("Lần sau chạy App, hãy chỉnh code để dùng 'best_model.pt' nhé!")
            else:
                print("Không tìm thấy file best.pt (Có thể quá trình train bị lỗi).")
        else:
            print("Không tìm thấy thư mục training.")
    else:
        print("Không tìm thấy thư mục runs.")

if __name__ == "__main__":
    main()
