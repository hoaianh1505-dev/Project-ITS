# Hướng Dẫn Huấn Luyện (Cách Đơn Giản Nhất)

Em đã chuẩn bị sẵn bộ công cụ "Tự Động Hóa". Anh chỉ cần làm **đúng 1 việc duy nhất** là kiếm ảnh.

## Quy Trình 3 Bước

### Bước 1: Gom Ảnh (Duy nhất bước này cần anh làm)
1.  Vào thư mục `data/raw`.
2.  Anh thấy sẵn 4 thư mục (cứu thương, công an, quân đội...).
3.  Lên Google tải ảnh xe tương ứng quăng vào đúng thư mục đó.
    *   *Ví dụ: Tải ảnh xe cứu thương -> Bỏ vào `xe_cuu_thuong_vietnam`*.
    *   *Lưu ý: Chỉ chọn ảnh có xe đó thôi, đừng chọn ảnh quá đông đúc.*
    
### Bước 2: Tự Động Dán Nhãn (Máy làm)
Chạy lệnh này, máy sẽ tự nhìn ảnh và biết cái xe nằm ở đâu để dán nhãn:

```bash
python src/auto_label.py
```

### Bước 3: Chia & Huấn Luyện (Máy làm)
Chạy 2 lệnh cuối cùng này là xong:

```bash
python src/split_data.py
python src/train.py
```

---
**Giải thích**: Code `auto_label` của em thông minh ở chỗ: Em dùng sẵn AI cơ bản để tìm "cái ô tô" trong ảnh anh tải về, rồi tự động sửa tên nó thành "Xe cứu thương" (tùy theo folder anh bỏ ảnh vào). Anh không cần vẽ tay nữa!
