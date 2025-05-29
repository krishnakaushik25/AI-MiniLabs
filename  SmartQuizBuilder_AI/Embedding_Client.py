import streamlit as st
from langchain_google_vertexai import VertexAIEmbeddings
import getpass
import os

class EmbeddingClient:
    def __init__(self, model_name, project, location):
        """
        Initialize the EmbeddingClient with the specified model, project, and location.
        
        :param model_name: Name of the embedding model to use.
        :param project: Google Cloud project ID.
        :param location: Google Cloud location.
        """
        self.client = VertexAIEmbeddings(
            model_name=model_name,
            project=project,
            location=location
        )
        
    def embed_query(self, query):
        """
        Embed a single query string.
        
        :param query: The text query to embed.
        :return: The embedding vectors for the query.
        """
        vectors = self.client.embed_query(query)
        return vectors
    
    def embed_documents(self, documents):
        """
        Embed a list of documents.
        
        :param documents: A list of documents to embed.
        :return: The embedding vectors for the documents.
        """
        try:
            return self.client.embed_documents(documents)
        except AttributeError:
            print("Method embed_documents not defined for the client.")
            return None

# Streamlit interface
if __name__ == "__main__":
    # Define the model, project, and location
    model_name = "textembedding-gecko@003"
    project = "gemini-quizzify-433204"
    location = "us-central1"

    # Create an instance of the EmbeddingClient
    embedding_client = EmbeddingClient(model_name, project, location)
    
    # Set up the Streamlit interface
    st.title('Text Embedding Display')
    query = st.text_input("Enter text to embed:", "Hello World!")
    
    if st.button("Get Embedding"):
        # Embed the query and display the results
        vectors = embedding_client.embed_query(query)
        if vectors:
            st.write(vectors)
            st.success("Successfully retrieved and displayed the embeddings.")
        else:
            st.error("Failed to retrieve embeddings.")