from pdf2image import convert_from_path
import cv2
import numpy as np
import pytesseract
import json


def deskew(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gray = cv2.bitwise_not(gray)
    coords = np.column_stack(np.where(gray > 0))
    angle = cv2.minAreaRect(coords)[-1]
    
    if angle < -45:
        angle = -(90 + angle)
    else:
        angle = -angle

    (h, w) = image.shape[:2]
    center = (w // 2, h // 2)
    M = cv2.getRotationMatrix2D(center, angle, 1.0)
    rotated = cv2.warpAffine(image, M, (w, h), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)

    return rotated

def extract_text_from_image(image):
    text = pytesseract.image_to_string(image)
    return text

pdf_file = ""
pages = convert_from_path(pdf_file)

# Create a list to store extracted text from all pages
extracted_text = []

page_number = 0

for page in pages:
    # Step 2: Preprocess the image (deskew)
    preprocessed_image = deskew(np.array(page))

    # Step 3: Extract text using OCR
    text = extract_text_from_image(preprocessed_image)
    clean_page = {"content":text,
                    "number":page_number,
                    "book":pdf_file}

    # extracted_text.append(text)
    extracted_text.append(clean_page)
    page_number += 1

with open("","w") as write:
    json.dump(extracted_text,write)

