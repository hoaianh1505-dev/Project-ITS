from ultralytics import YOLO
import cv2

class PriorityVehicleDetector:
    def __init__(self, model_path='yolov8n.pt'):
        """
        Initialize the YOLOv8 model.
        :param model_path: Path to the model weights. Defaults to 'yolov8n.pt' (automatically downloads).
        """
        print(f"Loading model from {model_path}...")
        self.model = YOLO(model_path)
        
        # Define target classes (COCO dataset indices for standard vehicles initially)
        # Note: Standard YOLOv8 is trained on COCO which has: car (2), motorcycle (3), airplane (4), bus (5), train (6), truck (7), boat (8).
        # It does NOT have specific 'ambulance', 'police car' classes by default. 
        # We will need to train a custom model for that.
        # for now, we detect all vehicles and will setup integration for custom model later.
        self.target_classes = [2, 3, 5, 7] # car, motorcycle, bus, truck

    def detect_and_draw(self, frame):
        """
        Detect objects in the frame and draw bounding boxes.
        :param frame: Input image/frame.
        :return: Tuple (results_list, annotated_frame)
        """
        results = self.model(frame, verbose=False)
        annotated_frame = results[0].plot() # YOLOv8 built-in plotting
        
        # Return the boxes for counting logic in main.py
        # results[0].boxes contains cls, conf, xyxy
        return results[0], annotated_frame
