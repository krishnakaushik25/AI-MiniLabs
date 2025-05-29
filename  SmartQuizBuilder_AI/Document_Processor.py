import streamlit as st
from langchain_community.document_loaders import PyPDFLoader
import os
import tempfile
import uuid

class DocumentProcessor:
    def __init__(self):
        """
        Initialize the DocumentProcessor class.
        """
        self.pages = []  # List to keep track of pages from all documents
    
    def ingest_documents(self):
        """
        Ingest PDF documents uploaded by the user.
        """
        # Render a file uploader widget to allow users to upload multiple PDF files
        uploaded_files = st.file_uploader("Upload PDF files", type="pdf", accept_multiple_files=True)
        
        if uploaded_files is not None:
            for uploaded_file in uploaded_files:
                # Generate a unique identifier to append to the file's original name
                unique_id = uuid.uuid4().hex
                original_name, file_extension = os.path.splitext(uploaded_file.name)
                temp_file_name = f"{original_name}_{unique_id}{file_extension}"
                temp_file_path = os.path.join(tempfile.gettempdir(), temp_file_name)

                # Write the uploaded PDF to a temporary file
                with open(temp_file_path, 'wb') as f:
                    f.write(uploaded_file.getvalue())

                # Process the temporary file using PyPDFLoader
                loader = PyPDFLoader(temp_file_path)
                extracted_pages = loader.load()
                self.pages.extend(extracted_pages)
 
                # Clean up by deleting the temporary file to free up space
                os.unlink(temp_file_path)
            
            # Display the total number of pages processed to the user
            st.write(f"Total pages processed: {len(self.pages)}")
           
        
if __name__ == "__main__":
    # Create an instance of the DocumentProcessor and ingest documents
    processor = DocumentProcessor()
    processor.ingest_documents()