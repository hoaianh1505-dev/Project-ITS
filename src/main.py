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
            "Ambulance": 0,
            "Fire Truck": 0,            "Police": 0,
            "Army": 0,
            "Civilian": 0
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
        
        self.btn_cam = ttk.Button(self.right_frame, text="📹 Bật Webcam", command=self.start_webcam)
        self.btn_cam.pack(fill=tk.X, pady=5)

        self.btn_stop = ttk.Button(self.right_frame, text="⏹ Dừng Lại", command=self.stop_video)
        self.btn_stop.pack(fill=tk.X, pady=5)

        # Statistics Section
        ttk.Separator(self.right_frame, orient='horizontal').pack(fill='x', pady=20)
        ttk.Label(self.right_frame, text="THỐNG KÊ (Thời gian thực)", style="Header.TLabel", font=("Helvetica", 16)).pack(pady=10)

        self.stat_labels = {}
        vehicle_colors = {
            "Fire Truck": "#e74c3c", # Red
            "Ambulance": "#f1c40f",  # Yellow
            "Police": "#3498db",     # Blue
            "Army": "#2ecc71",       # Green
            "Civilian": "#95a5a6"    # Grey
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

    def start_webcam(self):
        self.start_processing(0)

    def stop_video(self):
        self.is_running = False
        if self.cap:
            self.cap.release()
        self.video_label.config(image='', text="Đã dừng.")

    def start_processing(self, source):
        self.stop_video()
        self.video_source = source
        self.cap = cv2.VideoCapture(source)
        if not self.cap.isOpened():
            print("Error opening video")
            return
            
        self.is_running = True
        
        # Start separate thread for processing to keep UI responsive
        # Actually for simple Tkinter, using .after() loop is safer for UI updates than Threading
        self.process_loop()

    def process_loop(self):
        if not self.is_running:
            return

        ret, frame = self.cap.read()
        if ret:
            # Detect
            results, annotated_frame = self.detector.detect_and_draw(frame)
            
            # Count logic
            current_counts = {k: 0 for k in self.counts}
            
            # Determine if we are using Custom Model or Default YOLO
            # Custom model has classes 0,1,2,3...
            # Default YOLO has classes 2(car), 5(bus), 7(truck)...
            
            names = results.names # Dictionary of class names {0: 'person', ...} or {0: 'Fire Truck'...}
            is_custom_model = "xe_cuu_hoa_vietnam" in str(names) or len(names) < 10 # Heuristic
            
            if results.boxes:
                for box in results.boxes:
                    cls_id = int(box.cls[0])
                    
                    if is_custom_model:
                        # 0: Fire Truck, 1: Ambulance, 2: Police, 3: Army 
                        # (Referencing auto_label.py mapping)
                        if cls_id == 0: 
                            current_counts["Fire Truck"] += 1
                        elif cls_id == 1:
                            current_counts["Ambulance"] += 1
                        elif cls_id == 2:
                            current_counts["Police"] += 1
                        elif cls_id == 3:
                            current_counts["Army"] += 1
                        else:
                            current_counts["Civilian"] += 1
                    else:
                        # FALLBACK SIMULATION (Default YOLOv8n)
                        # 7: Truck -> Fire Truck
                        # 5: Bus -> Ambulance
                        # 2: Car -> Civilian
                        if cls_id == 7: 
                            current_counts["Fire Truck"] += 1
                        elif cls_id == 5: 
                            current_counts["Ambulance"] += 1
                        elif cls_id == 2: 
                            current_counts["Civilian"] += 1
                        elif cls_id == 3: # Motorcycle
                             current_counts["Civilian"] += 1
                        else:
                            # Other vehicles/objects
                            pass
            
            # Update Stats UI
            for k, v in current_counts.items():
                self.stat_labels[k].config(text=str(v))

            # Convert to RGB for Tkinter
            rgb_image = cv2.cvtColor(annotated_frame, cv2.COLOR_BGR2RGB)
            
            # Resize to fit label strictly if needed, or keep aspect ratio
            # Simple resize for now to fit the frame
            h, w, _ = rgb_image.shape
            display_w, display_h = 960, 720
            # Scale to fit
            scale = min(display_w/w, display_h/h)
            new_w, new_h = int(w*scale), int(h*scale)
            
            resized = cv2.resize(rgb_image, (new_w, new_h))
            img = Image.fromarray(resized)
            imgtk = ImageTk.PhotoImage(image=img)
            
            self.video_label.imgtk = imgtk # Keep reference
            self.video_label.config(image=imgtk, text="")
            
            # Call next frame
            self.root.after(10, self.process_loop)
        else:
            self.stop_video()
            self.video_label.config(text="Hết Video.")

    def change_model(self):
        selection = self.cbo_model.get()
        target_model = None
        
        if "Mặc Định" in selection:
            target_model = 'yolov8n.pt'
            print("Chuyển sang Model Mặc Định")
        else:
            if os.path.exists('best_model.pt'):
                target_model = 'best_model.pt'
                print("Chuyển sang Model Custom")
            else:
                messagebox.showerror("Lỗi", "Chưa tìm thấy file 'best_model.pt'.\nHãy chạy Train model trước!")
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
