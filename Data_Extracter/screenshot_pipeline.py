import pyautogui
import time
import pytesseract
pytesseract.pytesseract.tesseract_cmd = "/opt/homebrew/bin/tesseract"
from PIL import Image, ImageEnhance, ImageFilter
from datetime import datetime
import re
from transformers import AutoTokenizer, AutoModelForCausalLM
import json
import os


def load_images_from_folder(folder_path, allowed_extensions={"png", "jpg", "jpeg", "bmp", "gif"}):
    """Load all images from the specified folder."""
    images = []
    
    # List all files in the folder
    for filename in os.listdir(folder_path):
        # Check if the file is an image based on its extension
        if filename.lower().split(".")[-1] in allowed_extensions:
            image_path = os.path.join(folder_path, filename)
            try:
                img = Image.open(image_path)
                images.append(img)
                print(f"✅ Loaded: {filename}")
            except Exception as e:
                print(f"❌ Failed to load {filename}: {e}")
    
    return images



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
    res=[]
    folder_path = "/Users/felixmeng/Desktop/Coinbase_Hackathon/data/screenshots"  
    screenshots = load_images_from_folder(folder_path)
    print(f"📷 Total Images Loaded: {len(screenshots)}")

    for screenshot in screenshots:
        print("here")
        # screenshot = take_screenshot(i)
        screenshot = preprocess_image(screenshot)
        extracted_text = clean_text(extract_text(screenshot))
        data = {
        "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "text": extracted_text
        }
        res.append(data)
        print(extracted_text)
    with open("data/screen.json","w") as json_file:
        json.dump(res,json_file)


if __name__ == '__main__':
    # Example usage
    main()