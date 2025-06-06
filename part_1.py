import tkinter as tk
from tkinter import filedialog
from PIL import Image
import os

def select_and_show_image():
    root = tk.Tk()
    root.withdraw()  # Hide the root window

    file_path = filedialog.askopenfilename(
        title="Select an image file",
        filetypes=[("Image Files", "*.png *.jpg *.jpeg *.bmp *.gif *.webp")]
    )

    if not file_path:
        print("No file selected.")
        return

    try:
        img = Image.open(file_path)
        img.show()

        file_size_kb = os.path.getsize(file_path) / 1024
        file_name = os.path.basename(file_path)

        print(f"File Name: {file_name}")
        print(f"File Size: {file_size_kb:.2f} KB")
        print(f"Image Format: {img.format}")
        print(f"Dimensions: {img.width} x {img.height}")

    except Exception as e:
        print(f"Error opening image: {e}")

if __name__ == "__main__":
    select_and_show_image()
