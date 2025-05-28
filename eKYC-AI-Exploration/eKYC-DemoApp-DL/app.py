import os
import logging
import streamlit as st
from preprocess import read_image, extract_id_card, save_image
from ocr_engine import extract_text
from postprocess import extract_information,extract_information1
from face_verification import detect_and_extract_face, deepface_face_comparison, get_face_embeddings
from sql_connection import insert_records, fetch_records, check_duplicacy,insert_records_aadhar,fetch_records_aadhar,check_duplicacy_aadhar
import toml
import hashlib
logging_str = "[%(asctime)s: %(levelname)s: %(module)s]: %(message)s"
log_dir = "logs"
os.makedirs(log_dir, exist_ok=True)
logging.basicConfig(filename=os.path.join(log_dir,"ekyc_logs.log"), level=logging.INFO, format=logging_str, filemode="a")

config = toml.load("config.toml")
db_config = config.get("database", {})

db_user = db_config.get("user")
db_password = db_config.get("password")

def hash_id(id_value):
    hash_object = hashlib.sha256(id_value.encode())
    hashed_id = hash_object.hexdigest()
    return hashed_id

# Set wider page layout
def wider_page():
    max_width_str = "max-width: 1200px;"
    st.markdown(
        f"""
        <style>
            .reportview-container .main .block-container{{ {max_width_str} }}
        </style>
        """,
        unsafe_allow_html=True,
    )
    logging.info("Page layout set to wider configuration.")

# Customized Streamlit theme
def set_custom_theme():
    st.markdown(
        """
        <style>
            body {
                background-color: #f0f2f6; /* Set background color */
                color: #333333; /* Set text color */
            }
            .sidebar .sidebar-content {
                background-color: #ffffff; /* Set sidebar background color */
            }
        </style>
        """,
        unsafe_allow_html=True,
    )
    logging.info("Custom theme applied to Streamlit app.")


# Sidebar
def sidebar_section():
    st.sidebar.title("Select ID Card Type")
    option = st.sidebar.selectbox("", ("PAN","AADHAR"))
    logging.info(f"ID card type selected: {option}")
    return option

# Header
def header_section(option):
    if option == "AADHAR":
        st.title("Registration Using Aadhar Card")
        logging.info("Header set for Aadhar Card registration.")
    elif option == "PAN":
        st.title("Registration Using PAN Card")
        logging.info("Header set for PAN Card registration.")


# Main content
def main_content(image_file, face_image_file,option):
    if image_file is not None:
        face_image = read_image(face_image_file, is_uploaded=True)
        logging.info("Face image loaded.")
        if face_image is not None:
            image = read_image(image_file, is_uploaded=True)
            logging.info("ID card image loaded.")
            image_roi, _ = extract_id_card(image)
            logging.info("ID card ROI extracted.")
            face_image_path2 = detect_and_extract_face(img=image_roi)
            face_image_path1 = save_image(face_image, "face_image.jpg", path="data\\02_intermediate_data")
            logging.info("Faces extracted and saved.")
            is_face_verified = deepface_face_comparison(image1_path=face_image_path1, image2_path=face_image_path2)
            logging.info(f"Face verification status: {'successful' if is_face_verified else 'failed'}.")

            if is_face_verified:
                extracted_text = extract_text(image_roi)
                text_info = extract_information(extracted_text) if option == "PAN" else extract_information1(extracted_text)
                # print(extracted_text)
                logging.info("Text extracted and information parsed from ID card.")
                # print("Before",text_info['ID'])
                text_info['ID']=hash_id(text_info['ID'])
                # print("After",text_info['ID'])
                records = fetch_records(text_info) if option=="PAN" else fetch_records_aadhar(text_info)
                if records.shape[0] > 0:
                    st.write(records.shape)
                    st.write(records)
                is_duplicate = check_duplicacy(text_info) if option=="PAN" else check_duplicacy_aadhar(text_info)
                if is_duplicate:
                    st.write(f"User already present with ID {text_info['ID']}")
                else: 
                    # text_info["ID"]=hash_id(text_info["ID"])
                    st.write(text_info)
                    text_info['DOB'] = text_info['DOB'].strftime('%Y-%m-%d')
                    text_info['Embedding'] =  get_face_embeddings(face_image_path1)
                    insert_records(text_info) if option == "PAN" else insert_records_aadhar(text_info)
                    logging.info(f"New user record inserted: {text_info['ID']}")
                    
            else:
                st.error("Face verification failed. Please try again.")

        else:
            st.error("Face image not uploaded. Please upload a face image.")
            logging.error("No face image uploaded.")

    else:
        st.warning("Please upload an ID card image.")
        logging.warning("No ID card image uploaded.")

# Main function setup as previously provided...
def main():
    # Initialize connection.
    conn = st.connection(
    "local_db",
    type="sql",
    url="mysql://db_user:db_password@localhost:3306/ekyc"
)
    wider_page()
    set_custom_theme()
    option = sidebar_section()
    header_section(option)
    image_file = st.file_uploader("Upload ID Card")
    if image_file is not None:
        face_image_file = st.file_uploader("Upload Face Image")
        main_content(image_file, face_image_file,option)

if __name__ == "__main__":
    main()