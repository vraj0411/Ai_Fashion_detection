import tkinter as tk
from tkinter import filedialog
from PIL import Image
import os
import sys

MAX_WIDTH = 800
MAX_HEIGHT = 800

def process_image(input_path, output_path, output_format='JPEG', quality=85):
    try:
        img = Image.open(input_path)
    except FileNotFoundError:
        print("Error: Input file not found.")
        return False
    except OSError as e:
        print(f"Error: Cannot open image file (may be corrupted or unsupported): {e}")
        return False
    except Exception as e:
        print(f"Unexpected error opening image: {e}")
        return False

    # Show original size
    print(f"Original image size: {img.width} x {img.height}")

    # Resize if too large
    if img.width > MAX_WIDTH or img.height > MAX_HEIGHT:
        img.thumbnail((MAX_WIDTH, MAX_HEIGHT))
        print(f"Resized image size: {img.width} x {img.height}")
    else:
        print(f"Image size is within limits, no resize needed.")

    if output_format.upper() == 'JPEG' and img.mode != 'RGB':
        img = img.convert('RGB')

    try:
        img.save(output_path, format=output_format.upper(), quality=quality)
        print(f"Image saved successfully as: {output_path}")
        return True
    except PermissionError:
        print("Error: Permission denied when saving the file.")
        return False
    except Exception as e:
        print(f"Error saving image: {e}")
        return False

def main():
    try:
        root = tk.Tk()
        root.withdraw()  # Hide main window

        print("Select the image file to process:")
        input_path = filedialog.askopenfilename(
            title="Select Image",
            filetypes=[("Image Files", "*.png *.jpg *.jpeg *.bmp *.gif *.webp")]
        )
        if not input_path:
            print("No file selected. Exiting.")
            return

        folder, filename = os.path.split(input_path)
        name, ext = os.path.splitext(filename)

        # Get output format choice from user
        output_format = None
        while output_format not in ['JPEG', 'PNG']:
            choice = input("Choose output format (jpg/png): ").strip().lower()
            if choice in ['jpg', 'jpeg']:
                output_format = 'JPEG'
            elif choice == 'png':
                output_format = 'PNG'
            else:
                print("Invalid choice, please enter 'jpg' or 'png'.")

        out_ext = '.jpg' if output_format == 'JPEG' else '.png'
        output_path = os.path.join(folder, f"{name}_processed{out_ext}")

        success = process_image(input_path, output_path, output_format)
        if success:
            print(f"Processing complete. File saved at: {output_path}")
        else:
            print("Processing failed.")

    except Exception as e:
        print(f"Unexpected error occurred: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
