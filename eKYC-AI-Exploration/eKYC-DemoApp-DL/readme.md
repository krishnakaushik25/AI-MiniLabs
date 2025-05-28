# E-KYC Project
Welcome to the E-KYC project! This project leverages cutting-edge techniques in computer vision, natural language processing, convolutional neural networks (CNNs), and long short-term memory networks (LSTMs) to facilitate automatic Know Your Customer (KYC) processes. 

## Overview

The E-KYC web application provides an interactive user interface where users can upload their ID card (limited to Aadhar and PAN cards at the moment) and a photograph of their face. The app then internally processes the provided ID card to extract the face and matches it with the uploaded photograph. 

### Features

1. **Face Verification**: The app computes the face from the provided ID card using Haarcascade and matches it with the uploaded photograph. If the verification status is successful, subsequent operations are carried out; otherwise, an error is generated.
   
## Face Verification Demo

![E-KYC-FACE VERIFICATION DEMO](https://github.com/abhishekiiitbh2903/E-KYC-/blob/main/assets/Face%20Verification.gif)


Herein, I have uploaded an ID card of my dad and an image of myself. As a result, the face verification fails, and as stated above, the subsequent codes do not execute.

2. **Optical Character Recognition (OCR)**: If face verification is successful, the app uses EasyOCR with a predefined threshold value to extract text from the ID card.
3. **Database Interaction**: The extracted text and face embeddings are checked for duplicacy before being inserted into the database. If the user is already registered, the SQL query is not executed, and the fetched result is returned.
4. **Face Embeddings**: The app uses FaceNet from DeepFace to retrieve face embeddings, which are also stored in the database.

## Full Workflow of web app

![Full Workflow](https://github.com/abhishekiiitbh2903/E-KYC-/blob/main/assets/Full%20Workflow.gif)

I first uploaded my Aadhar ID and a photo of my dad. The app flagged a warning as face verification failed, and subsequent code didn't execute. Then, I uploaded my own face image, the verification succeeded, and my data was inserted into the database. To check for duplicacy and confirm my data was correctly inserted, I reuploaded my face image. The response indicated that a person with my ID already exists in the database, validating proper database handling and ensuring no data duplicacy.


### Technologies Used

- **Computer Vision**: For face detection and verification.
- **Natural Language Processing**: For text extraction and processing.
- **Convolutional Neural Networks (CNNs)**: For image processing tasks.
- **Long Short-Term Memory Networks (LSTMs)**: For handling sequential data.
- **EasyOCR**: For OCR operations.
- **DeepFace**: For face embeddings.
- **Haarcascade**: For detecting faces in ID cards.

## Upcoming Improvements

1. **Live Face Detection**: Instead of taking a face image from the user, the app will detect the face image live using the device's camera.
2. **Data Privacy**: Currently, original values are stored in the database. In future updates, sensitive data (like original IDs) will be hashed before storage to ensure privacy even if the database is compromised.
**[COMPLETED]**

## Prerequisites

Ensure you have the following installed:
- Python 12.0
- MySQL server

## Setup Instructions

1. **Clone the Repository**:
    ```sh
    https://github.com/abhishekiiitbh2903/E-KYC-.git
    cd E-KYC-
    ```

2. **Create a Virtual Environment**:
    ```sh
    python -m venv .venv 
    ```

3. **Activate the Virtual Environment**:
    - On Windows:
      ```sh
      .\.venv\Scripts\activate
      ```
    - On macOS/Linux:
      ```sh
      source .venv/bin/activate
      ```

4. **Install the Required Packages**:
    ```sh
    pip install -r requirements.txt
    ```

5. **Create the `config.toml` File**:
    In the root directory of the project (same directory as `app.py`), create a file named `config.toml` and add the following content to it:

    ```toml
    [database]
    user = "your_username"
    password = "your_password"
    host = "localhost"
    database = "your_database_name"
    ```

    Replace `"your_username"`, `"your_password"`, and `"your_database_name"` with your actual MySQL credentials.

6. **Run the Application**:
    ```sh
    streamlit run app.py
    ```

## Important Notes

- **Security**: Ensure that your `config.toml` file is included in the `.gitignore` file to prevent sensitive information from being uploaded to any public repository.

- **.gitignore**: The `.gitignore` file should include the following lines to ignore the virtual environment and configuration files:

    ```plaintext
    # Ignore virtual environment directory
    .venv/
    
    # Ignore config.toml file
    config.toml
    ```

## Logging

The application logs various events and errors for easier debugging and monitoring. Logs are stored in the `logs` directory. Ensure this directory exists in your local setup or create it manually if it does not exist.

**Note**: The `logs` directory has not been included in the repository to prevent accidental exposure of sensitive information or potential data breaches from logs related to your local system.

Proper logging practices have been implemented throughout the project to ensure comprehensive error tracking and system monitoring.


## Troubleshooting

- **Database Connection Issues**: Ensure your MySQL server is running and the credentials in `config.toml` are correct.
- **Dependencies**: If you encounter issues with missing packages, ensure all required packages are installed by running `pip install -r requirements.txt`.

Feel free to open an issue if you encounter any problems or have questions about the setup process.


## Author

This project is authored by Abhishek Singh, a final year B.Tech CSE undergraduate at IIIT Bhagalpur. You can reach me at abhishekrathore1806@gmail.com.

## Contributing

I am open to contributions! If you can work on the possible areas of improvement or have other enhancements in mind, feel free to fork the repository, make your changes, and initiate a pull request. If the changes are legitimate and add value to the project, I will merge them.

Happy coding! 😊
