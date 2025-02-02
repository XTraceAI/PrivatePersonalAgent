import pyautogui
import time
import pytesseract
pytesseract.pytesseract.tesseract_cmd = "/opt/homebrew/bin/tesseract"
from PIL import Image, ImageEnhance, ImageFilter
from datetime import datetime
import re
from transformers import AutoTokenizer, AutoModelForCausalLM
import json


def take_screenshot(i):
    x, y = 0, 130  # Top-left corner (excluding the address bar)
    width, height = 1920, 900  # Adjust based on screen resolution
    screenshot = pyautogui.screenshot(region=(x, y, width, height))

    screenshot.save(f"data/screenshots/screenshot_real{i}.png")
    return screenshot

def preprocess_image(image):
    """Enhance and clean the image for better OCR accuracy."""
    image = image.convert("L")  # Convert to grayscale
    image = image.filter(ImageFilter.SHARPEN)  # Sharpen text
    image = ImageEnhance.Contrast(image).enhance(2)  # Increase contrast
    return image

def extract_text(image):
    image = preprocess_image(image)
    text = pytesseract.image_to_string(image, config="--psm 6")  # Adjust PSM mode
    return text

def clean_text(text):
    """Basic cleaning: removes unwanted characters and formatting."""
    text = re.sub(r"\n+", " ", text)  # Replace multiple newlines with a space
    text = re.sub(r"[^\x00-\x7F]+", " ", text)  # Remove non-ASCII characters
    text = re.sub(r"\s+", " ", text).strip()    # Remove extra spaces
    return text

def save_data(text, output_json="transcription.json"):
    """Saves the transcribed text with a timestamp as JSON."""
    data = {
        "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "text": text
    }

    with open(output_json, "w") as json_file:
        json.dump(data, json_file, indent=4)

    print(f"✅ Transcription saved to {output_json}")

def main():
    i=0
    time.sleep(1)
    res=[]
    while True:
        screenshot = take_screenshot(i)
        screenshot = preprocess_image(screenshot)
        extracted_text = clean_text(extract_text(screenshot))
        data = {
        "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "text": extracted_text
        }
        res.append(data)
        time.sleep(1)
        if i>=2:
            break
        i+=1
        print(i)
    with open("data/screen.json","w") as json_file:
        json.dump(res,json_file)


if __name__ == '__main__':
    main()