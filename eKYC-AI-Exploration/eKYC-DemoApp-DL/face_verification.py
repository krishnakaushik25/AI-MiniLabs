from deepface import DeepFace
import cv2
import os
import logging
from utils import file_exists, read_yaml

logging_str = "[%(asctime)s: %(levelname)s: %(module)s]: %(message)s"
log_dir = "logs"
os.makedirs(log_dir, exist_ok=True)
logging.basicConfig(filename=os.path.join(log_dir,"ekyc_logs.log"), level=logging.INFO, format=logging_str, filemode="a")


config_path = "config.yaml"
config = read_yaml(config_path)

artifacts = config['artifacts']
cascade_path = artifacts['HAARCASCADE_PATH']
output_path = artifacts['INTERMIDEIATE_DIR']

def detect_and_extract_face(img):
    logging.info("Extracting face...")
    # Read the image
    # img = cv2.imread(image_path)

    # Convert the image to grayscale (Haar cascade works better with grayscale images)
    gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Load the Haar cascade classifier
    face_cascade = cv2.CascadeClassifier(cascade_path)

    # Detect faces in the image
    faces = face_cascade.detectMultiScale(gray_img, scaleFactor=1.1, minNeighbors=5)

    # Find the face with the largest area
    max_area = 0
    largest_face = None
    for (x, y, w, h) in faces:
        area = w * h
        if area > max_area:
            max_area = area
            largest_face = (x, y, w, h)

    # Extract the largest face
    if largest_face is not None:
        (x, y, w, h) = largest_face
        # extracted_face = img[y:y+h, x:x+w]
        
        # Increase dimensions by 15%
        new_w = int(w * 1.50)
        new_h = int(h * 1.50)
        
        # Calculate new (x, y) coordinates to keep the center of the face the same
        new_x = max(0, x - int((new_w - w) / 2))
        new_y = max(0, y - int((new_h - h) / 2))

        # Extract the enlarged face
        extracted_face = img[new_y:new_y+new_h, new_x:new_x+new_w]

        # Convert the extracted face to RGB
        # extracted_face_rgb = cv2.cvtColor(extracted_face, cv2.COLOR_BGR2RGB)

        
        current_wd = os.getcwd()
        filename = os.path.join(current_wd, output_path, "extracted_face.jpg")

        if os.path.exists(filename):
            # Remove the existing file
            os.remove(filename)

        cv2.imwrite(filename, extracted_face)
        # print(f"Extracted face saved at: {filename}")
        logging.info(f"Extracted face saved at: {filename}")
        return filename

        # return extracted_face_rgb

    else:
        logging.warning("No face detected in the image")
        return None
    

# ---------- Debugging ----------------

file_path="data/01_raw_data/pan.jpeg"
img=cv2.imread(file_path)
detect_and_extract_face(img)


def deepface_face_comparison(image1_path, image2_path):
    logging.info("Verifying the images....")
    img1_exists = file_exists(image1_path)
    img2_exists = file_exists(image2_path)

    if not(img1_exists or img2_exists):
        logging.warning("One or both image paths do not exist")
        # print("Check the path for the images provided")
        return False
    
    verfication = DeepFace.verify(img1_path=image1_path, img2_path=image2_path)

    if len(verfication) > 0 and verfication['verified']:
        logging.info("Faces are verified as the same person")
        # print("Faces are verified")
        return True
    else:
        logging.info("Faces are not verified as the same person")
        return False
    
#--------------Debugging------------

# file_path1="data/02_intermediate_data/face.jpg"
# file_path2="data/02_intermediate_data/face2.jpg"

# print(deepface_face_comparison(file_path1,file_path2))

def get_face_embeddings(image_path):
    logging.info(f"Retrieving face embeddings from image: {image_path}")

    # Check if image exists
    if not file_exists(image_path):
        logging.warning(f"Image path does not exist: {image_path}")
        return None
    
    # Retrieve face embeddings using DeepFace library (Facenet model)
    embedding_objs = DeepFace.represent(img_path=image_path, model_name="Facenet")

    # Extract the embedding vector
    embedding = embedding_objs[0]["embedding"]

    if len(embedding) > 0:
        logging.info("Face embeddings retrieved successfully")
        return embedding
    else:
        logging.warning("Failed to retrieve face embeddings")
        return None
    

# file_path1="data/02_intermediate_data/face.jpg"
# print(get_face_embeddings(file_path1))