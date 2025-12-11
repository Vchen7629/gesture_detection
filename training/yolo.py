from ultralytics import YOLO
from pathlib import Path
import cv2

def train_model():
    # Path configs
    script_dir = Path(__file__).parent
    dataset_config_path = script_dir / "../dataset/dataset_config.yaml"

    model = YOLO("yolo11n.pt")

    train_results = model.train(
        data=str(dataset_config_path.resolve()),
        epochs=100,
        device=0
    )

    metrics = model.val()

def live_detection():
    script_dir = Path(__file__).parent
    trained_model = script_dir / "../runs/detect/train7/weights/best.pt"

    # Loading trained model
    model = YOLO(str(trained_model.resolve()))

    # Open webcam
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("Error: Could not open webcam")
        return

    print("Starting live detection. Press 'q' to quit.")

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Error: Could not read frame")
            break

        # Run prediction on the frame
        results = model.predict(source=frame, conf=0.25, verbose=False)

        # Get the annotated frame with bounding boxes
        annotated_frame = results[0].plot()

        # Display the frame
        cv2.imshow('YOLO Live Detection', annotated_frame)

        # Press 'q' to quit
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    # train_model() 
     live_detection() 