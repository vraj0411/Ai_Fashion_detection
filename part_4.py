import os
import cv2
import torch
import numpy as np
from tkinter import Tk, filedialog
from ultralytics import YOLO
from sklearn.cluster import KMeans
from collections import Counter
from fpdf import FPDF
import pyttsx3

# --- SETTINGS ---
MODEL_PATH = '/Users/vrajalpeshkumarmodi/Downloads/Fashion/runs/detect/fashion-yolov8/weights/best.pt'
CLASS_LABELS = {
    1: 'formal',
    2: 'sports wear',
    3: 'shirt',
    4: 'pant',
    5: 'dress',
    6: 'shoes',
    7: 'accessories'
}

COLOR_NAMES = {
    'red': (255, 0, 0), 'green': (0, 128, 0), 'blue': (0, 0, 255), 'yellow': (255, 255, 0),
    'orange': (255, 165, 0), 'purple': (128, 0, 128), 'pink': (255, 192, 203), 'black': (0, 0, 0),
    'white': (255, 255, 255), 'gray': (128, 128, 128), 'brown': (139, 69, 19), 'cyan': (0, 255, 255),
    'magenta': (255, 0, 255)
}

def closest_color(requested_color):
    min_colors = {}
    for name, rgb in COLOR_NAMES.items():
        r_c, g_c, b_c = rgb
        rd = (r_c - requested_color[0]) ** 2
        gd = (g_c - requested_color[1]) ** 2
        bd = (b_c - requested_color[2]) ** 2
        min_colors[(rd + gd + bd)] = name
    return min_colors[min(min_colors.keys())]

def get_dominant_color(image):
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    image = image.reshape((image.shape[0] * image.shape[1], 3))
    kmeans = KMeans(n_clusters=3, n_init=10)
    kmeans.fit(image)
    counts = Counter(kmeans.labels_)
    center_colors = kmeans.cluster_centers_
    dominant_color = center_colors[counts.most_common(1)[0][0]]
    return tuple(map(int, dominant_color))

def complementary_color_name(color_name):
    complementary = {
        'red': 'green', 'green': 'red', 'blue': 'orange', 'orange': 'blue', 'purple': 'yellow',
        'yellow': 'purple', 'pink': 'gray', 'black': 'white', 'white': 'black', 'gray': 'pink',
        'brown': 'cyan', 'cyan': 'brown', 'magenta': 'green'
    }
    return complementary.get(color_name, 'neutral')

def detect_fashion(image_path):
    model = YOLO(MODEL_PATH)
    results = model(image_path)[0]
    image = cv2.imread(image_path)

    detections = []
    color_info = {}

    for box in results.boxes:
        cls_id = int(box.cls[0])
        label = CLASS_LABELS.get(cls_id, 'unknown')
        x1, y1, x2, y2 = map(int, box.xyxy[0])
        roi = image[y1:y2, x1:x2]
        if label in ['shirt', 'pant']:
            dom_color = get_dominant_color(roi)
            color_name = closest_color(dom_color)
            comp_color = complementary_color_name(color_name)
            color_info[label] = {
                'dominant': color_name,
                'complementary': comp_color
            }
        detections.append(label)

    return detections, color_info

def generate_pdf_report(image_path, color_info, report_path):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt="Fashion Detection Report", ln=True, align='C')
    pdf.ln(10)

    pdf.image(image_path, w=100)
    pdf.ln(10)

    for item, data in color_info.items():
        text = f"Detected: {item.capitalize()}\nColor: {data['dominant']}\nSuggested Complementary Color: {data['complementary']}\n"
        pdf.multi_cell(0, 10, txt=text)

    pdf.output(report_path)

def speak_text(color_info):
    engine = pyttsx3.init()
    engine.setProperty('rate', 135)
    for item, data in color_info.items():
        message = f"Detected {item}, with color {data['dominant']}. You can pair it with {data['complementary']}."
        engine.say(message)
    engine.runAndWait()

def main():
    root = Tk()
    root.withdraw()
    image_path = filedialog.askopenfilename(title="Select an Image")
    if not image_path:
        print("No image selected.")
        return

    detections, color_info = detect_fashion(image_path)

    print("Detected Items:", detections)
    print("Color Info:", color_info)

    report_path = os.path.splitext(image_path)[0] + "_report.pdf"
    generate_pdf_report(image_path, color_info, report_path)

    print(f"PDF Report saved to: {report_path}")
    speak_text(color_info)

if __name__ == "__main__":
    main()