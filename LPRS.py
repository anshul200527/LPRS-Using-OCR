import pytesseract
import cv2
import imutils
import os
import re
import pandas as pd
import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image
import numpy as np

# Tesseract config..
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

dataset_path = "owndataset1.csv"  
try:
    dataset = pd.read_csv(dataset_path)
    print("Dataset loaded successfully.")
    dataset.columns = dataset.columns.str.strip() 
except Exception as e:
    print(f"Error loading dataset: {e}")
    exit()

def preprocess_image(image):
    image = imutils.resize(image, width=500)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (5, 5), 0)
    gray = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)
    return gray

def clean_license_plate(text):
    text = re.sub(r'[^A-Z0-9]', '', text.upper())
    print(f"Cleaned License Plate: {text}")  
    return text

def find_owner(license_plate):
    print(f"looking for: {license_plate}")  
    result = dataset[dataset['LICENSE PLATE NUMBER'] == license_plate]
    if not result.empty:
        owner_name = result.iloc[0]['OWNERS NAME']
        contact_no = result.iloc[0]['CONTACT NO.']
        return {"Owner Name": owner_name, "Contact No.": contact_no}
    return None

def load_image():
    file_path = filedialog.askopenfilename(title="Select an Image", filetypes=[("Image Files", "*.jpg;*.jpeg;*.png")])
    if file_path:
        process_image(file_path)

def process_image(file_path):
    try:
        image = cv2.imread(file_path)
        if image is None:
            raise Exception("Failed to load image.")
        
        gray = preprocess_image(image)
        
        # Perform OCR
        config = "--psm 7"  
        text = pytesseract.image_to_string(gray, config=config, lang="eng")
        print(f"Extracted Text: {text}")  # Debug print
        cleaned_plate = clean_license_plate(text)
    
        owner_info = find_owner(cleaned_plate)
        
        # Display result
        if owner_info:
            result_text = f"Owner: {owner_info['Owner Name']}\nContact: {owner_info['Contact No.']}"
        else:
            result_text = "No matching license plate found in the dataset."
        
        result_label.config(text=result_text)
        cv2.imshow("Processed Image", gray)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")

root = tk.Tk()
root.title("License Plate Recognition")

root.geometry("500x500")

load_button = tk.Button(root, text="Load Image", command=load_image)
load_button.pack(pady=20)

result_label = tk.Label(root, text="Results will be shown here.", justify=tk.LEFT)
result_label.pack(pady=20)

# GUI
root.mainloop()
