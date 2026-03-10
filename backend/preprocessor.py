import cv2
import numpy as np
from PIL import Image

def preprocess_image_for_ocr(image: Image.Image) -> Image.Image:
    """
    Takes a PIL Image, applies OpenCV preprocessing (grayscale, binarization, noise removal)
    to improve OCR accuracy, and returns a PIL Image.
    """
    # Convert PIL directly to OpenCV format (numpy array)
    open_cv_image = np.array(image)
    
    # Convert RGB to BGR (OpenCV format) if image has 3 channels
    if len(open_cv_image.shape) == 3 and open_cv_image.shape[2] == 3:
        # Convert to grayscale
        gray = cv2.cvtColor(open_cv_image, cv2.COLOR_RGB2GRAY)
    else:
        gray = open_cv_image

    # Apply adaptive thresholding to binarize the image (good for variable lighting like photos of labels)
    binary = cv2.adaptiveThreshold(
        gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2
    )
    
    # Optional: Denoising/Blur to remove small imperfections
    denoised = cv2.medianBlur(binary, 3)
    
    # Convert back to PIL Image
    result_image = Image.fromarray(denoised)
    return result_image
