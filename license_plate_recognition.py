import pytesseract
import cv2
import imutils

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

image = cv2.imread('image.jpg') 
if image is None:
    print("Error: Image not found!")
    exit()
else:
    print("Image loaded successfully.")

image = imutils.resize(image, width=500)

gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Apply adaptive thresholding for better OCR results
new_image = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)

config = "--psm 11"  # Page segmentation mode (adjust based on your image)

# Perform OCR using Tesseract
try:
    text = pytesseract.image_to_string(new_image, config=config)
    print("Extracted Text:")
    print(text)
except Exception as e:
    print("Error during OCR:", str(e))

# Display the processed image (optional)
cv2.imshow("Processed Image", new_image)
cv2.waitKey(0)
cv2.destroyAllWindows()
