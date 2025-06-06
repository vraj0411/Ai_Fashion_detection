from ultralytics import YOLO
import cv2
from tkinter import filedialog, Tk
import os

# Mapping from your dataset (class IDs start from 1)
class_map = {
    1: "formal",       # class 1
    2: "sports wear",  # class 2
    3: "shirt",        # class 3
    4: "pant",         # class 4
    5: "dress",        # class 5
    6: "shoes",        # class 6
    7: "accessories"   # class 7
}

# Load YOLOv8 model (update the path if needed)
model = YOLO("/Users/vrajalpeshkumarmodi/Downloads/Fashion/runs/detect/fashion-yolov8/weights/best.pt")

# Function to decide final type based on rules
def classify_fashion(classes_detected):
    formal_related = {1, 3, 4, 5}
    sports_related = {2}
    if formal_related.intersection(classes_detected):
        return "formal"
    elif sports_related.intersection(classes_detected):
        return "sports wear"
    else:
        return "sports wear"

# Draw bounding boxes
def draw_box(img, box, label, conf):
    x1, y1, x2, y2 = map(int, box)
    cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
    text = f"{label} {conf:.2f}"
    cv2.putText(img, text, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 0, 0), 2)

# File selection
Tk().withdraw()
file_path = filedialog.askopenfilename(title="Select Image or Video",
                                       filetypes=[("Media files", "*.jpg *.jpeg *.png *.mp4 *.avi")])

if not file_path:
    print("❌ No file selected.")
    exit()

# IMAGE MODE
if file_path.lower().endswith((".jpg", ".jpeg", ".png")):
    results = model(file_path)[0]
    img = cv2.imread(file_path)
    detected_classes = set()

    for box, cls_id, conf in zip(results.boxes.xyxy, results.boxes.cls, results.boxes.conf):
        cls = int(cls_id.item()) + 1  # YOLOv8 class starts from 0
        label = class_map.get(cls, "unknown")
        detected_classes.add(cls)
        draw_box(img, box, label, conf.item())

    overall = classify_fashion(detected_classes)
    cv2.putText(img, f"Overall: {overall}", (10, 40), cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 0, 255), 3)

    out_path = file_path.rsplit('.', 1)[0] + "_output.jpg"
    cv2.imwrite(out_path, img)
    print(f"✅ Image saved at: {out_path}")
    cv2.imshow("Output", img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

# VIDEO MODE
elif file_path.lower().endswith((".mp4", ".avi")):
    cap = cv2.VideoCapture(file_path)
    width  = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps    = cap.get(cv2.CAP_PROP_FPS)
    out_path = file_path.rsplit('.', 1)[0] + "_output.mp4"
    out = cv2.VideoWriter(out_path, cv2.VideoWriter_fourcc(*'mp4v'), fps, (width, height))

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        results = model(frame)[0]
        detected_classes = set()

        for box, cls_id, conf in zip(results.boxes.xyxy, results.boxes.cls, results.boxes.conf):
            cls = int(cls_id.item()) + 1
            label = class_map.get(cls, "unknown")
            detected_classes.add(cls)
            draw_box(frame, box, label, conf.item())

        overall = classify_fashion(detected_classes)
        cv2.putText(frame, f"Overall: {overall}", (10, 40), cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 0, 255), 3)

        out.write(frame)
        cv2.imshow("Video Output", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    out.release()
    cv2.destroyAllWindows()
    print(f"✅ Video saved at: {out_path}")

else:
    print("❌ Unsupported file format.")
