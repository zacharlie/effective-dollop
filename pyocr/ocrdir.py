import os
from PIL import Image
import pytesseract
import sys

script_dir = os.path.dirname(os.path.abspath(__file__))
image_dir = os.path.join(script_dir, "ocrimg")
output_file = os.path.join(script_dir, "ocr_output.txt")

# Set Tesseract executable path
# TESSERACT_PATH = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
# TESSERACT_PATH = "/usr/bin/tesseract"


if not TESSERACT_PATH:
    raise Exception(
        "TESSERACT_PATH is not defined. Please set the path to the Tesseract executable."
    )

pytesseract.pytesseract.tesseract_cmd = TESSERACT_PATH

image_files = [
    os.path.join(image_dir, f)
    for f in os.listdir(image_dir)
    if f.endswith(".png")
    or f.endswith(".webp")
    or f.endswith(".jpg")
    or f.endswith(".jpeg")
]

with open(output_file, "w") as f:
    for image_file in image_files:
        image = Image.open(image_file)
        text = pytesseract.image_to_string(image)
        condition = True
        # condition = True if "loremipsum" in text.lower().replace(" ", "") else False
        if condition:
            # f.write(f"File: {image_file}\n")
            f.write(text + "\n")
