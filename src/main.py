import cv2
import argparse
from detection import PriorityVehicleDetector

def main():
    parser = argparse.ArgumentParser(description='Priority Vehicle Recognition')
    parser.add_argument('--source', type=str, default='0', help='Video source: 0 for webcam, or path to video file')
    args = parser.parse_args()

    # Initialize Detector
    detector = PriorityVehicleDetector()

    # Open Video Source
    source = args.source
    if source.isdigit():
        source = int(source)
    
    cap = cv2.VideoCapture(source)

    if not cap.isOpened():
        print(f"Error: Could not open video source {source}")
        return

    print("Starting detection... Press 'q' to quit.")

    while True:
        ret, frame = cap.read()
        if not ret:
            print("End of video stream.")
            break

        # Run detection
        results_frame = detector.detect_and_draw(frame)

        # Display result
        cv2.imshow('Priority Vehicle Recognition', results_frame)

        # Exit on 'q'
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main()
