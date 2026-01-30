import cv2
import argparse
import tkinter as tk
from tkinter import filedialog, ttk, messagebox
from PIL import Image, ImageTk
from detection import PriorityVehicleDetector
import threading
import os
import time

class TrafficApp:
    def __init__(self, root, model_path=None):
        self.root = root
        self.root.title("Hệ Thống Nhận Diện Phương Tiện Ưu Tiên")
        self.root.geometry("1400x850")
        self.root.configure(bg="#2c3e50")

        # Initialize Detector
        self.detector = PriorityVehicleDetector(model_path=model_path)
        
        # State variables
        self.video_source = None
        self.is_running = False
        self.cap = None
        self.counts = {
            "Xe Cứu Thương": 0,
            "Xe Cứu Hỏa": 0,
            "Xe CSGT": 0,
            "Xe Quân Đội": 0,
            "Xe Dân Sự": 0
        }

        self.setup_ui()

    def setup_ui(self):
        # --- Left Panel: Video Feed ---
        self.left_frame = tk.Frame(self.root, bg="#34495e", width=960, height=720)
        self.left_frame.pack(side=tk.LEFT, padx=20, pady=20, fill=tk.BOTH, expand=True)
        self.left_frame.pack_propagate(False) # Prevent shrinking

        self.video_label = tk.Label(self.left_frame, bg="black", text="Vui lòng chọn Video hoặc Camera", fg="white")
        self.video_label.pack(fill=tk.BOTH, expand=True)

        # --- Right Panel: Dashboard ---
        self.right_frame = tk.Frame(self.root, bg="#2c3e50", width=350)
        self.right_frame.pack(side=tk.RIGHT, fill=tk.Y, padx=10, pady=20)

        # Styles
        style = ttk.Style()
        style.theme_use('clam')
        style.configure("TButton", font=("Helvetica", 12), padding=10)
        style.configure("Header.TLabel", font=("Helvetica", 20, "bold"), background="#2c3e50", foreground="#ecf0f1")
        style.configure("Stat.TLabel", font=("Helvetica", 14), background="#2c3e50", foreground="white")

        # Header
        ttk.Label(self.right_frame, text="BẢNG ĐIỀU KHIỂN", style="Header.TLabel").pack(pady=(0, 20))

        # --- Model Selection ---
        ttk.Label(self.right_frame, text="Chọn Model:", font=("Helvetica", 12), background="#2c3e50", foreground="#ecf0f1").pack(anchor='w', padx=5)
        self.cbo_model = ttk.Combobox(self.right_frame, values=[
            "Model Mặc Định (Giả lập)", 
            "Model Tự Train (AI Việt Nam)"
        ], state="readonly", font=("Helvetica", 11))
        self.cbo_model.current(0) # Default
        self.cbo_model.pack(fill=tk.X, pady=5)
        
        self.btn_change_model = ttk.Button(self.right_frame, text="🔄 Chuyển Model", command=self.change_model)
        self.btn_change_model.pack(fill=tk.X, pady=(0, 15))

        # Controls
        self.btn_files = ttk.Button(self.right_frame, text="📂 Chọn Video File", command=self.select_video)
        self.btn_files.pack(fill=tk.X, pady=5)

        self.btn_img = ttk.Button(self.right_frame, text="🖼️ Chọn Ảnh (Image)", command=self.select_image)
        self.btn_img.pack(fill=tk.X, pady=5)
        
        self.btn_cam = ttk.Button(self.right_frame, text="📹 Bật Webcam", command=self.start_webcam)
        self.btn_cam.pack(fill=tk.X, pady=5)

        self.btn_stop = ttk.Button(self.right_frame, text="⏹ Dừng Lại", command=self.stop_video)
        self.btn_stop.pack(fill=tk.X, pady=5)

        # Statistics Section
        ttk.Separator(self.right_frame, orient='horizontal').pack(fill='x', pady=20)
        ttk.Label(self.right_frame, text="THỐNG KÊ (Thời gian thực)", style="Header.TLabel", font=("Helvetica", 16)).pack(pady=10)

        self.stat_labels = {}
        vehicle_colors = {
            "Xe Cứu Hỏa": "#e74c3c", # Red
            "Xe Cứu Thương": "#f1c40f",  # Yellow
            "Xe CSGT": "#3498db",     # Blue
            "Xe Quân Đội": "#2ecc71",       # Green
            "Xe Dân Sự": "#95a5a6"    # Grey
        }

        for v_type, color in vehicle_colors.items():
            frame = tk.Frame(self.right_frame, bg="#2c3e50")
            frame.pack(fill=tk.X, pady=5)
            
            # Label
            lbl_name = tk.Label(frame, text=v_type, font=("Helvetica", 14, "bold"), fg=color, bg="#2c3e50", anchor='w')
            lbl_name.pack(side=tk.LEFT)
            
            # Count Value
            lbl_count = tk.Label(frame, text="0", font=("Helvetica", 18, "bold"), fg="white", bg="#2c3e50")
            lbl_count.pack(side=tk.RIGHT)
            
            self.stat_labels[v_type] = lbl_count

    def select_video(self):
        source = filedialog.askopenfilename(filetypes=[("Video files", "*.mp4 *.avi *.mkv"), ("All files", "*.*")])
        if source:
            self.start_processing(source)

    def select_image(self):
        source = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg *.jpeg *.png *.bmp"), ("All files", "*.*")])
        if source:
            self.process_single_image(source)

    def start_webcam(self):
        self.start_processing(0)

    def stop_video(self):
        self.is_running = False
        if self.cap:
            self.cap.release()
            self.cap = None
        self.video_label.config(image='', text="Đã dừng / Chờ xử lý...")

    def process_single_image(self, source):
        self.stop_video()
        self.video_source = source
        
        frame = cv2.imread(source)
        if frame is None:
            messagebox.showerror("Lỗi", "Không thể đọc file ảnh này!")
            return
            
        results, annotated_frame = self.detector.detect_and_draw(frame)
        self.update_dashboard(results, annotated_frame)

    def start_processing(self, source):
        self.stop_video()
        self.video_source = source
        self.cap = cv2.VideoCapture(source)
        if not self.cap.isOpened():
            print("Error opening video")
            return
            
        self.is_running = True
        self.detected_vehicles = {} # Reset unique vehicle store
        if hasattr(self, 'track_history'):
            self.track_history.clear()
            
        self.process_loop()

    def process_loop(self):
        if not self.is_running:
            return

        ret, frame = self.cap.read()
        if ret:
            results, annotated_frame = self.detector.detect_and_draw(frame)
            self.update_dashboard(results, annotated_frame)
            self.root.after(10, self.process_loop)
        else:
            self.stop_video()
            self.video_label.config(text="Hết Video.")

    def update_dashboard(self, results, annotated_frame):
        # Lazy init for image mode or first run
        if not hasattr(self, 'detected_vehicles'):
            self.detected_vehicles = {}
        
        # Initialize track history if not exists (Lazy init)
        if not hasattr(self, 'track_history'):
            self.track_history = {}

        names = results.names 
        is_custom_model = "xe cuu thuong vietnam" in str(names) or "xe_cuu_thuong_vietnam" in str(names) or len(names) < 10

        if results.boxes:
            for box in results.boxes:
                cls_id = int(box.cls[0])
                
                # --- VOTING LOGIC START ---
                # Check if we have a tracking ID (only available in Video mode)
                track_id = int(box.id[0]) if box.id is not None else -1 # Use -1 for untracked objects
                
                final_cls_id = cls_id # Default to current frame if no tracking
                
                if track_id != -1:
                    # Initialize history list for this vehicle ID
                    if track_id not in self.track_history:
                        self.track_history[track_id] = []
                    
                    # Add current class to history
                    self.track_history[track_id].append(cls_id)
                    
                    # Keep only last 30 frames (approx 1-2 seconds)
                    if len(self.track_history[track_id]) > 30:
                        self.track_history[track_id].pop(0)
                        
                    # Vote: Find the most frequent class in history
                    from collections import Counter
                    most_common = Counter(self.track_history[track_id]).most_common(1)
                    final_cls_id = most_common[0][0]
                # --- VOTING LOGIC END ---

                # Determine Label
                label_name = "Xe Dân Sự"
                if is_custom_model:
                     # 0: Ambulance, 1: Police, 2: Fire Truck, 3: Army
                    if final_cls_id == 2: label_name = "Xe Cứu Hỏa"
                    elif final_cls_id == 0: label_name = "Xe Cứu Thương"
                    elif final_cls_id == 1: label_name = "Xe CSGT"
                    elif final_cls_id == 3: label_name = "Xe Quân Đội"
                else:
                    # FALLBACK
                    if final_cls_id == 7: label_name = "Xe Cứu Hỏa"
                    elif final_cls_id == 5: label_name = "Xe Cứu Thương"
                    elif final_cls_id == 2: label_name = "Xe Dân Sự"
                    elif final_cls_id == 3: label_name = "Xe Dân Sự"

                # DEBUG: Print what we found
                # print(f"DEBUG: TrackID={track_id} -> {label_name}")

                # Update Persistent Store
                if track_id != -1:
                    self.detected_vehicles[track_id] = label_name
                else:
                    # For image mode (no tracking ID), just increment a temp counter or similar?
                    # Actually for image mode we likely want simple counting.
                    # But since this function handles both, let's just cheat for Image mode:
                    # Image mode usually runs once. We can generate a random ID or just count raw.
                    # BETTER: For image mode, we don't have IDs. We should just display what's on screen.
                    pass

        # Calculate Totals
        # Default with 0
        final_counts = {
            "Xe Cứu Thương": 0, "Xe Cứu Hỏa": 0, "Xe CSGT": 0, "Xe Quân Đội": 0, "Xe Dân Sự": 0
        }
        
        # Aggregate from unique tracked vehicles
        if self.detected_vehicles:
            for v_name in self.detected_vehicles.values():
                if v_name in final_counts:
                    final_counts[v_name] += 1
        
        # Verify: If we are in image mode (no tracking), self.detected_vehicles might be empty or consistent.
        # If image mode, track_id is -1. We shouldn't use detected_vehicles for -1 blindly or we get only 1 car.
        # FIX: If results.boxes has no IDs (Image mode), fallback to instant count.
        has_tracking = results.boxes is not None and results.boxes and results.boxes[0].id is not None
        
        if not has_tracking and results.boxes:
             # Image Mode / No Tracking Fallback
             # Clear persistent storage to avoid mixing previous video data? 
             # No, start_processing clears it.
             # Just recount frame from scratch
             final_counts = {k: 0 for k in final_counts} # Reset
             for box in results.boxes:
                 cls = int(box.cls[0])
                 # Simplified mapping for fallback
                 lbl = "Xe Dân Sự"
                 if is_custom_model:
                     if cls==2: lbl="Xe Cứu Hỏa"
                     elif cls==0: lbl="Xe Cứu Thương"
                     elif cls==1: lbl="Xe CSGT"
                     elif cls==3: lbl="Xe Quân Đội"
                 else:
                     if cls==7: lbl="Xe Cứu Hỏa"
                     elif cls==5: lbl="Xe Cứu Thương"
                 
                 if lbl in final_counts: final_counts[lbl] += 1

        # Update Stats UI
        for k, v in final_counts.items():
            self.stat_labels[k].config(text=str(v))

        # Convert to RGB for Tkinter
        rgb_image = cv2.cvtColor(annotated_frame, cv2.COLOR_BGR2RGB)
        
        h, w, _ = rgb_image.shape
        display_w, display_h = 960, 720
        scale = min(display_w/w, display_h/h)
        new_w, new_h = int(w*scale), int(h*scale)
        
        resized = cv2.resize(rgb_image, (new_w, new_h))
        img = Image.fromarray(resized)
        imgtk = ImageTk.PhotoImage(image=img)
        
        self.video_label.imgtk = imgtk
        self.video_label.config(image=imgtk, text="")

    def change_model(self):
        selection = self.cbo_model.get()
        target_model = None
        
        if "Mặc Định" in selection:
            target_model = 'models/yolov8n.pt'
            print("Chuyển sang Model Mặc Định")
        else:
            if os.path.exists('models/best_model.pt'):
                target_model = 'models/best_model.pt'
                print("Chuyển sang Model Custom")
            else:
                messagebox.showerror("Lỗi", "Chưa tìm thấy file 'models/best_model.pt'.\nHãy chạy Train model trước!")
                self.cbo_model.current(0)
                return

        # Reload detector
        try:
            self.detector = PriorityVehicleDetector(model_path=target_model)
            messagebox.showinfo("Thành công", f"Đã chuyển sang: {selection}")
        except Exception as e:
            messagebox.showerror("Lỗi", f"Không nạp được model: {e}")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--source', type=str, default=None, help='Video path')
    parser.add_argument('--model', type=str, default=None, help='Path to .pt model file')
    args = parser.parse_args()
    
    root = tk.Tk()
    app = TrafficApp(root, model_path=args.model)
    root.mainloop()

if __name__ == '__main__':
    main()
