import sys
import os
import streamlit as st

# Adjust the path to include the root directory of your project
sys.path.append(os.path.abspath('../../'))

# Import necessary classes from other tasks
from Document_Processor import DocumentProcessor
from Embedding_Client import EmbeddingClient
from Chroma_Collection_Creator import ChromaCollectionCreator
from io import StringIO

if __name__ == "__main__":
    st.header("📝 PDF Quizify")

    # Configuration for EmbeddingClient
    embed_config = {
        "model_name": "textembedding-gecko@003",
        "project": "gemini-quizzify-433204",
        "location": "us-central1"
    }
    
    # Set persistence directory
    persist_directory = "chroma_persistence_directory"
    
    # Initialize components
    processor = DocumentProcessor()
    embedding_client = EmbeddingClient(**embed_config)
    chroma_creator = ChromaCollectionCreator(processor, embedding_client, persist_directory=persist_directory)
    
    # Ingest documents via DocumentProcessor (this handles file uploads)
    processor.ingest_documents()

    # Form to submit quiz details
    with st.form("Load Data to Chroma"):
        st.subheader("Quiz Builder")
        st.write("Enter the topic for the quiz and number of questions, then click Generate!")

        topic_input = st.text_input("Enter Quiz Topic")
        
        # Replace number input with a slider
        num_questions = st.slider("Number of Questions", min_value=1, max_value=50, value=10)
        
        submitted = st.form_submit_button("Generate a Quiz!")

        if submitted:
            # Check if any documents were processed
            if processor.pages:
                st.success(f"Processed {len(processor.pages)} page(s) successfully!")
            else:
                st.error("Please upload at least one PDF to generate the quiz.")
                st.stop()

            # Check if Chroma collection already exists
            # Load existing Chroma collection from disk, if it exists
            if not chroma_creator.db:
                chroma_creator.create_chroma_collection()
                st.success("New Chroma collection successfully created!", icon="✅")
                
            # Query the Chroma collection for the entered topic
            document = chroma_creator.query_chroma_collection(topic_input)
            
            if document:
                with st.container():
                    st.header("Query Chroma for Topic, top Document: ")
                    st.write(document)
            else:
                st.error("No matching documents found for the quiz topic.")