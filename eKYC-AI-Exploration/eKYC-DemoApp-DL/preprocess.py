import cv2
import numpy as np
import os
import logging
from utils import read_yaml, file_exists

# Logging configuration
logging_str = "[%(asctime)s: %(levelname)s: %(module)s]: %(message)s"
log_dir = "logs"
os.makedirs(log_dir, exist_ok=True)
logging.basicConfig(filename=os.path.join(log_dir, "ekyc_logs.log"), level=logging.INFO, format=logging_str, filemode="a")

# ---------------DEBUGGING--------------
# Testing the functionality of logging (Easier for Debugging)
# # Example log messages
# logging.info("This is an info message.")
# logging.warning("This is a warning message.")
# logging.error("This is an error message.")

config_path = "config.yaml"
config = read_yaml(config_path)
# print(config)

artifacts = config['artifacts']
intermediate_dir_path = artifacts['INTERMIDEIATE_DIR']
conour_file_name = artifacts['CONTOUR_FILE']
# print(intermediate_dir_path)

def read_image(image_path, is_uploaded=False):
    if is_uploaded:
        try:
            # Read image using OpenCV
            image_bytes = image_path.read()
            img = cv2.imdecode(np.frombuffer(image_bytes, np.uint8), cv2.IMREAD_COLOR)
            if img is None:
                logging.info("Failed to read image: {}".format(image_path))
                raise Exception("Failed to read image: {}".format(image_path))
            return img
        except Exception as e:
            logging.info(f"Error reading image: {e}")
            print("Error reading image:", e)
            return None
    else:
        try:
            img = cv2.imread(image_path)
            if img is None:
                logging.info("Failed to read image: {}".format(image_path))
                raise Exception("Failed to read image: {}".format(image_path))
            return img
        except Exception as e:
            logging.info(f"Error reading image: {e}")
            print("Error reading image:", e)
            return None

# ---------------DEBUGGING-----------

# Example usage of read_image
# image_path = "data/02_intermediate_data/id_card.png"
# image = read_image(image_path, is_uploaded=False)

# if image is not None:
#     cv2.imshow("Image", image)
#     cv2.waitKey(0)
#     cv2.destroyAllWindows()
# else:
#     print("Failed to load image.")


def extract_id_card(img):

    # Convert image to grayscale
    # ---------------------- Reduces Computational Complexity involved ----------------
    gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Noise reduction
    #----This helps in creating smoother contours and reduces the chances of detecting false contours------
    blur = cv2.GaussianBlur(gray_img, (5, 5), 0)

    # Adaptive thresholding
    # -------- This helps in distinguishing the foreground (ID card) from the background -------
    thresh = cv2.adaptiveThreshold(blur, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 11, 2)

    # --------- MORPHOLOGICAL EXPRESSIONS ------------------
    # Apply morphological operations
    # kernel = np.ones((5, 5), np.uint8)

    # # Apply opening to remove small noise
    # thresh = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel)

    # # Apply closing to fill small holes
    # thresh = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)

    # Find contours

    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Select the largest contour (assuming the ID card is the largest object)
    largest_contour = None
    largest_area = 0
    for cnt in contours:
        area = cv2.contourArea(cnt)
        if area > largest_area:
            largest_contour = cnt
            largest_area = area

    # If no large contour is found, assume no ID card is present
    if not largest_contour.any():
        return None

    # Get bounding rectangle of the largest contour
    x, y, w, h = cv2.boundingRect(largest_contour)

    logging.info(f"contours are found at, {(x, y, w, h)}")
    # logging.info("Area largest_area)

    # Apply additional filtering (optional):
    # - Apply bilateral filtering for noise reduction
    # filtered_img = cv2.bilateralFiltering(img[y:y+h, x:x+w], 9, 75, 75)
    # - Morphological operations (e.g., erosion, dilation) for shape refinement
    current_wd = os.getcwd()
    filename = os.path.join(current_wd,intermediate_dir_path, conour_file_name)
    contour_id = img[y:y+h, x:x+w]
    is_exists = file_exists(filename)
    if is_exists:
        # Remove the existing file
        os.remove(filename)

    cv2.imwrite(filename, contour_id)

    return contour_id, filename


# ----------- DEBUGGING ----------------
# # Example usage of extract_id_card
# image_path = "data/02_intermediate_data/deskew.png"
# image = cv2.imread(image_path)

# if image is not None:
#     extracted_image, file_path = extract_id_card(image)
#     if extracted_image is not None:
#         logging.info(f"Extracted ID card saved to: {file_path}")
#     else:
#         logging.error("No ID card detected in the image.")
# else:
#     logging.error("Failed to load image.")



# ------ Saving the Image ----------

def save_image(image, filename, path="."):

  # Construct the full path
  full_path = os.path.join(path, filename)
  is_exists = file_exists(full_path)
  if is_exists:
        # Remove the existing file
        os.remove(full_path)

  # Save the image using cv2.imwrite
  cv2.imwrite(full_path, image)

  logging.info(f"Image saved successfully: {full_path}")
  return full_path

# -------------- DEBUGGING ------------------

# # Example image (a simple black square)
# image = np.zeros((100, 100, 3), dtype=np.uint8)

# # Save the image
# saved_path = save_image(image, "black_square.jpg", "images")
