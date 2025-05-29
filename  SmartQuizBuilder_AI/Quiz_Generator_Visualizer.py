import streamlit as st
import os
import sys
import json
import time

# Adjust the path to include the root directory of your project
sys.path.append(os.path.abspath('../../'))

# Import necessary classes from other tasks
from Document_Processor import DocumentProcessor
from Embedding_Client import EmbeddingClient
from Chroma_Collection_Creator import ChromaCollectionCreator
from langchain.output_parsers import ResponseSchema, StructuredOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_google_vertexai import VertexAI

class QuizGenerator:
    def __init__(self, topic=None, num_questions=1, vectorstore=None):
        """
        Initializes the QuizGenerator with a required topic, the number of questions for the quiz,
        and an optional vectorstore for querying related information.
        
        :param topic: The topic for the quiz. Defaults to "General Knowledge" if not provided.
        :param num_questions: Number of questions for the quiz. Cannot exceed 10.
        :param vectorstore: Optional vectorstore for querying related information.
        """
        if not topic:
            self.topic = "General Knowledge"
        else:
            self.topic = topic

        if num_questions > 10:
            raise ValueError("Number of questions cannot exceed 10.")
        self.num_questions = num_questions

        self.vectorstore = vectorstore
        self.llm = None
        self.question_bank = []  # Initialize the question bank to store questions

        # Structured output schema and parser for formatted JSON output
        self.response_schemas = [
            ResponseSchema(name="question", description="The quiz question."),
            ResponseSchema(name="choices", description="List of multiple choice options with keys."),
            ResponseSchema(name="answer", description="The correct answer from the choices."),
            ResponseSchema(name="explanation", description="Explanation of the correct answer.")
        ]
        self.output_parser = StructuredOutputParser.from_response_schemas(self.response_schemas)
        self.format_instructions = self.output_parser.get_format_instructions()

        # Enhanced prompt template from task_7
        self.prompt_template = """
            You are a subject matter expert on the topic: {topic}

            Follow the instructions to create a quiz question:
            1. Generate a question based on the topic provided.
            2. Provide 4 multiple choice answers.
            3. Specify the correct answer.
            4. Explain why the correct answer is right.

            {format_instructions}

            The choices must be returned in this format:
            [
                {{"key": "A", "value": "<choice A>"}},
                {{"key": "B", "value": "<choice B>"}},
                {{"key": "C", "value": "<choice C>"}},
                {{"key": "D", "value": "<choice D>"}}
            ]

            The answer must refer to the key from the choices list.

            Context: {context}
        """

    def init_llm(self):
        """
        Initializes and configures the Large Language Model (LLM) for generating quiz questions.
        """
        self.llm = VertexAI(
            model_name="gemini-pro",
            temperature=0.8,
            max_output_tokens=500
        )

    def generate_question_with_vectorstore(self):
        """
        Generates a quiz question based on the topic provided using a vectorstore.
        
        :return: The generated quiz question.
        """
        if not self.llm:
            self.init_llm()
        if not self.vectorstore:
            raise ValueError("Vectorstore not provided.")

        from langchain_core.runnables import RunnablePassthrough, RunnableParallel

        # Use the database's retriever
        retriever = self.vectorstore.db.as_retriever()

        prompt = PromptTemplate(
            template=self.prompt_template,
            input_variables=["topic", "context"],
            partial_variables={"format_instructions": self.format_instructions}
        )

        setup_and_retrieval = RunnableParallel(
            {"context": retriever, "topic": RunnablePassthrough()}
        )
        chain = setup_and_retrieval | prompt | self.llm | self.output_parser

        response = chain.invoke(self.topic)
        return response

    def generate_quiz(self) -> list:
        """
        Generates a quiz by creating multiple questions based on the topic.
        
        :return: A tuple containing the list of generated questions and the raw responses.
        """
        self.question_bank = []
        raw_responses = []  # Store raw LLM responses

        for _ in range(self.num_questions):
            for _ in range(0, 10):
                response = self.generate_question_with_vectorstore()
                raw_responses.append(response)  # Append raw response for later display

                # No need to parse the response with json.loads() since it's already a dictionary
                question = response

                # Validate and store the unique question
                if self.validate_question(question):
                    print("Successfully generated unique question")
                    self.question_bank.append(question)
                    break  # Exit retry loop once a valid question is generated
                else:
                    print("Duplicate or invalid question detected.")

                # Add a delay to avoid exceeding quotas
                time.sleep(20)  # Wait 20 seconds before the next request

        return self.question_bank, raw_responses

    def validate_question(self, question: dict) -> bool:
        """
        Validates the uniqueness of the generated quiz question.
        
        :param question: The generated quiz question.
        :return: True if the question is unique, False otherwise.
        """
        is_unique = True
        question_text = question.get('question')
        if not question_text:
            is_unique = False
        else:
            for existing_question in self.question_bank:
                if existing_question['question'] == question_text:
                    is_unique = False

        return is_unique

# Test Generating the Quiz
if __name__ == "__main__":

    embed_config = {
        "model_name": "textembedding-gecko@003",
        "project": "gemini-quizzify-433204",
        "location": "us-central1"
    }

    # Set persistence directory
    persist_directory = "chroma_persistence_directory"

    screen = st.empty()
    with screen.container():
        st.header("Quiz Builder")
        processor = DocumentProcessor()
        processor.ingest_documents()

        embed_client = EmbeddingClient(**embed_config)  # Initialize from Task 4

        # Initialize ChromaCollectionCreator with persistence
        chroma_creator = ChromaCollectionCreator(processor, embed_client, persist_directory=persist_directory)

        # Load existing Chroma collection from disk, if it exists
        if not chroma_creator.db:
            chroma_creator.create_chroma_collection()
            st.success("New Chroma collection successfully created!", icon="✅")
            
        question = None
        question_bank = None
        raw_responses = None

        with st.form("Load Data to Chroma"):
            st.subheader("Quiz Builder")
            st.write("Select PDFs for Ingestion, the topic for the quiz, and click Generate!")

            topic_input = st.text_input("Topic for Generative Quiz", placeholder="Enter the topic of the document")
            questions = st.slider("Number of Questions", min_value=1, max_value=10, value=1)

            submitted = st.form_submit_button("Submit")
            if submitted:
                generator = QuizGenerator(topic_input, questions, chroma_creator)
                question_bank, raw_responses = generator.generate_quiz()
                question = question_bank[0]

    if question_bank:
        screen.empty()
        with st.container():
            st.header("Generated Quiz Questions:")
            for question in question_bank:
                st.write(question['question'])
                st.write(f"Choices: {question['choices']}")
                st.write(f"Answer: {question['answer']}")
                st.write(f"Explanation: {question['explanation']}")

            st.header("Raw LLM Response:")
            for raw_response in raw_responses:
                st.write(raw_response)