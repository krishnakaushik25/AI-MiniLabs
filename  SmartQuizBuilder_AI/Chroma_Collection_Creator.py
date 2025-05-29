import sys
import os
import streamlit as st

# Adjust the path to include the root directory of your project
sys.path.append(os.path.abspath('../../'))

# Import necessary classes from other tasks
from Document_Processor import DocumentProcessor
from Embedding_Client import EmbeddingClient

# Import Task libraries
from langchain_core.documents import Document
from langchain.text_splitter import CharacterTextSplitter
from langchain_community.vectorstores import Chroma

class ChromaCollectionCreator:
    def __init__(self, processor, embed_model, persist_directory=None):
        """
        Initializes the ChromaCollectionCreator with a DocumentProcessor instance, embeddings configuration,
        and an optional persist directory for Chroma collection persistence.
        
        :param processor: Instance of DocumentProcessor.
        :param embed_model: Instance of EmbeddingClient.
        :param persist_directory: Optional directory for persistence.
        """
        self.processor = processor      # DocumentProcessor from Task 3
        self.embed_model = embed_model  # EmbeddingClient from Task 4
        self.persist_directory = persist_directory  # Optional directory for persistence
        self.db = None                  # Chroma collection
        
        # Load the existing Chroma collection if it exists
        if self.persist_directory and os.path.exists(self.persist_directory):
            self.db = Chroma(persist_directory=self.persist_directory, embedding_function=self.embed_model)
            st.success("Loaded existing Chroma collection from disk!", icon="✅")
    
    def create_chroma_collection(self):
        """
        Create a Chroma collection from the documents processed by the DocumentProcessor instance,
        with persistence support if a directory is provided.
        """
        # Check for processed documents
        if len(self.processor.pages) == 0:
            st.error("No documents found!", icon="🚨")
            return

        # Split documents into text chunks
        splitter = CharacterTextSplitter(separator=" ", chunk_size=1024, chunk_overlap=100)
        texts = []

        for page in self.processor.pages:
            text_chunks = splitter.split_text(page.page_content)
            for text in text_chunks:
                doc = Document(page_content=text, metadata={"source": "local"})
                texts.append(doc)

        if texts:
            st.success(f"Successfully split pages into {len(texts)} documents!", icon="✅")
        else:
            st.error("Failed to split pages!", icon="🚨")
            return

        # Create the Chroma Collection with persistence
        if self.persist_directory:
            self.db = Chroma.from_documents(
                documents=texts,
                embedding=self.embed_model,
                persist_directory=self.persist_directory  # Use persistence
            )
            self.db.persist()  # Persist the collection to disk
        else:
            self.db = Chroma.from_documents(
                documents=texts,
                embedding=self.embed_model
            )

        if self.db:
            st.success("Successfully created Chroma Collection!", icon="✅")
        else:
            st.error("Failed to create Chroma Collection!", icon="🚨")
    
    def query_chroma_collection(self, query) -> Document:
        """
        Queries the created Chroma collection for documents similar to the query.
        
        :param query: The query string to search for.
        :return: The most similar document or None if no match is found.
        """
        if self.db:
            docs = self.db.similarity_search_with_relevance_scores(query)
            if docs:
                return docs[0]
            else:
                st.error("No matching documents found!", icon="🚨")
        else:
            st.error("Chroma Collection has not been created!", icon="🚨")

if __name__ == "__main__":
    st.header("Quizify - Chroma Collection Creator")
    
    # Initialize the DocumentProcessor
    processor = DocumentProcessor()  # Initialize from Task 3
    processor.ingest_documents()

    # Define embedding configuration
    embed_config = {
        "model_name": "textembedding-gecko@003",
        "project": "gemini-quizzify-433204",
        "location": "us-central1"
    }

    # Initialize the EmbeddingClient
    embed_client = EmbeddingClient(**embed_config)  # Initialize from Task 4

    # Set persistence directory
    persist_directory = "chroma_persistence_directory"
    
    # Initialize the ChromaCollectionCreator
    chroma_creator = ChromaCollectionCreator(processor, embed_client, persist_directory=persist_directory)

    # Streamlit form for loading data to Chroma
    with st.form("Load Data to Chroma"):
        st.write("Select PDFs for Ingestion, then click Submit")

        submitted = st.form_submit_button("Submit")
        if submitted:
            chroma_creator.create_chroma_collection()