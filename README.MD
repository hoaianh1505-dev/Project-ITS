# 🚗 Hệ Thống Nhận Diện Phương Tiện Ưu Tiên (ProjectITS)

Dự án xây dựng hệ thống giao thông thông minh (ITS) ứng dụng thị giác máy tính để phát hiện và phân loại các phương tiện ưu tiên trong điều kiện giao thông tại Việt Nam. Hệ thống sử dụng mô hình **YOLOv8**, thư viện **OpenCV** và giao diện đồ họa **Tkinter**.

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![YOLOv8](https://img.shields.io/badge/YOLOv8-Ultralytics-green.svg)
![OpenCV](https://img.shields.io/badge/OpenCV-Computer_Vision-red.svg)

---

## 🎯 Tính Năng Chính

- **🔍 Nhận diện đa lớp**: Phát hiện chính xác 4 loại phương tiện ưu tiên theo luật giao thông Việt Nam:
  - 🚑 **Xe cứu thương** (Ambulance)
  - 🚒 **Xe cứu hỏa** (Fire Truck)
  - 🚓 **Xe cảnh sát giao thông** (Traffic Police)
  - 🪖 **Xe quân đội** (Army)
- **⚡ Xử lý thời gian thực**: Hoạt động mượt mà trên Webcam hoặc Video file.
- **📊 Thống kê trực quan**: Đếm và hiển thị số lượng từng loại xe ngay trên màn hình dashboard.
- **🖥️ Giao diện thân thiện**: GUI xây dựng bằng Tkinter dễ sử dụng cho người vận hành.
- **🔄 Cơ chế Dual-Model**: Dễ dàng chuyển đổi giữa Model mặc định (Pre-trained) và Model tự huấn luyện (Custom).

---

## 🛠️ Công Nghệ Sử Dụng

- **Ngôn ngữ**: Python 3.8+
- **Core AI**: YOLOv8 (Ultralytics) - Mô hình Deep Learning nhận diện vật thể.
- **Xử lý ảnh**: OpenCV, Pillow.
- **Giao diện (GUI)**: Tkinter.
- **Dữ liệu**: Custom Dataset thu thập từ môi trường giao thông Việt Nam.

---

## 📁 Cấu Trúc Dự Án & Ý Nghĩa

```
ProjectITS/
├── 📂 data/                    # Chứa dữ liệu hình ảnh
│   ├── raw/                    # Ảnh thô thu thập ban đầu
│   ├── train/                  # Ảnh dùng để huấn luyện model
│   └── val/                    # Ảnh dùng để đánh giá/kiểm thử
├── 📂 docs/                    # Tài liệu báo cáo đồ án
├── 📂 models/                  # Nơi chứa các "bộ não" AI
│   ├── best_model.pt           # Model đã được train (Custom)
│   └── yolov8n.pt              # Model gốc của YOLO (Base)
├── 📂 src/                     # Mã nguồn chính
│   ├── main.py                 # File CHÍNH: Chạy ứng dụng giao diện
│   ├── detection.py            # File xử lý logic nhận diện AI
│   ├── collect_data.py         # Tool cắt ảnh từ video để làm dữ liệu
│   ├── auto_label.py           # Tool gán nhãn tự động (hỗ trợ train)
│   ├── split_data.py           # Tool chia dữ liệu train/val
│   ├── train.py                # Script huấn luyện mô hình
│   └── run_training.py         # Script chạy toàn bộ quy trình train
├── 📂 videos/                  # Video clip mẫu để test
├── data.yaml                   # File cấu hình đường dẫn và tên các class
└── requirements.txt            # Danh sách thư viện cần cài đặt
```

---

## 🚀 Hướng Dẫn Cài Đặt

### 1. Yêu cầu hệ thống
- Hệ điều hành: Windows/Linux/MacOS
- Python: Phiên bản 3.8 trở lên
- Webcam (nếu muốn chạy thử chế độ camera)

### 2. Cài đặt môi trường
```bash
# Clone dự án về máy
git clone https://github.com/hoaianh1505-dev/Project-ITS.git
cd Project-ITS

# Tạo môi trường ảo (Khuyên dùng)
python -m venv .venv
# Kích hoạt môi trường:
# Windows:
.venv\Scripts\activate
# Linux/Mac:
# source .venv/bin/activate

# Cài đặt các thư viện cần thiết
pip install -r requirements.txt
```

---

## ▶️ Hướng Dẫn Sử Dụng

### 1. Chạy ứng dụng nhận diện (Inference)
Đây là chức năng chính để demo sản phẩm.
```bash
python src/main.py
```
*Giao diện sẽ hiện lên, bạn có thể chọn "Mở file Video" hoặc "Bật Webcam" để bắt đầu.*

### 2. Quy trình huấn luyện lại Model (Training Pipeline)
Nếu bạn muốn model thông minh hơn hoặc nhận diện thêm loại xe mới, hãy làm theo các bước:

1.  **Thu thập dữ liệu**: Bỏ video quay được vào thư mục `videos/` và chạy `collect_data.py` để cắt thành ảnh.
2.  **Gán nhãn**: Chạy `auto_label.py` để máy tự gán nhãn sơ bộ, sau đó dùng các tool (như LabelImg) để sửa lại cho đúng.
3.  **Chia dữ liệu**: Chạy `split_data.py` để chia ảnh vào thư mục `train` và `val`.
4.  **Huấn luyện**: Chạy lệnh sau để bắt đầu train:
    ```bash
    python src/run_training.py
    ```
5.  **Kết quả**: File model mới sẽ được lưu tại `models/best_model.pt`.

---

## 👨‍💻 Tác Giả & Liên Hệ

**Đề tài: Hệ thống nhận diện phương tiện ưu tiên trong ITS**
*   **Thực hiện bởi**: Nhóm nghiên cứu ProjectITS
*   **Email**: anhd78428@gmail.com
*   **GitHub**: [@hoaianh1505-dev](https://github.com/hoaianh1505-dev)

---
*Dự án phục vụ mục đích học tập và nghiên cứu nhập môn Thị giác máy tính (Computer Vision).*