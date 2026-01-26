# Priority Vehicle Recognition (ProjectITS)

Hệ thống nhận diện phương tiện ưu tiên (Xe cứu thương, Cứu hỏa, Cảnh sát, Xe quân đội) sử dụng YOLOv8.

## Cài đặt

1.  **Yêu cầu**: Python 3.8+
2.  **Cài đặt thư viện**:
    ```bash
    pip install -r requirements.txt
    ```

## Chạy chương trình

Mặc định sử dụng Webcam (0):
```bash
python src/main.py
```

Chạy với video file:
```bash
python src/main.py --source "path/to/video.mp4"
```

## Cấu trúc dự án
- `src/main.py`: File chạy chính.
- `src/detection.py`: Xử lý nhận diện (Model YOLO).
- `models/`: Chứa file weights (.pt) sau khi train.