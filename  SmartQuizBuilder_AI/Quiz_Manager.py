import streamlit as st
import os
import sys
import time

# Adjust the path to include the root directory of your project
sys.path.append(os.path.abspath('../../'))

# Import necessary classes from other tasks
from Document_Processor import DocumentProcessor
from Embedding_Client import EmbeddingClient
from Chroma_Collection_Creator import ChromaCollectionCreator
from Quiz_Generator import QuizGenerator

# QuizManager class to manage quiz state and navigation
class QuizManager:
    def __init__(self, questions: list):
        """
        Initializes the QuizManager with a list of questions.
        
        :param questions: List of quiz questions.
        """
        self.questions = questions
        self.total_questions = len(questions)

    def get_question_at_index(self, index: int):
        """
        Retrieves the question at the specified index.
        
        :param index: Index of the question to retrieve.
        :return: The question at the specified index.
        """
        valid_index = index % self.total_questions
        return self.questions[valid_index]

    def next_question_index(self, direction=1):
        """
        Moves to the next question index.
        
        :param direction: Direction to move (1 for next, -1 for previous).
        :return: The new question index.
        """
        current_index = st.session_state.get("question_index", 0)
        new_index = (current_index + direction) % self.total_questions
        st.session_state["question_index"] = new_index
        return new_index

if __name__ == "__main__":
    # Embed config
    embed_config = {
        "model_name": "textembedding-gecko@003",
        "project": "gemini-quizzify-433204",
        "location": "us-central1"
    }

    # Initialize Streamlit UI
    screen = st.empty()

    # Only show the form if the quiz hasn't started
    if "quiz_manager" not in st.session_state:
        with screen.container():
            st.header("📝 PDF Quizify")

            # Form to generate quiz
            with st.form("Load Data to Chroma"):
                st.subheader("Quiz Manager")
                st.write("Select PDFs for Ingestion, the topic for the quiz, and click Generate!")

                processor = DocumentProcessor()
                processor.ingest_documents()

                embed_client = EmbeddingClient(**embed_config)

                topic_input = st.text_input("Topic for Generative Quiz", placeholder="Enter the topic of the document")
                questions_count = st.slider("Number of Questions", min_value=1, max_value=10, value=1)
                submitted = st.form_submit_button("Submit")

                # Generate quiz questions
                if submitted:
                    persist_directory = "chroma_persistence_directory"
                    chroma_creator = ChromaCollectionCreator(processor, embed_client, persist_directory=persist_directory)
                    
                    if not chroma_creator.db:
                        chroma_creator.create_chroma_collection()
                        st.success("New Chroma collection successfully created!", icon="✅")

                    generator = QuizGenerator(topic_input, questions_count, chroma_creator)
                    question_bank, raw_responses = generator.generate_quiz()

                    st.session_state["quiz_manager"] = QuizManager(question_bank)
                    st.session_state["question_index"] = 0
                    st.session_state["is_submitting"] = False  # Initialize submission state
                    screen.empty()  # Clear the screen completely once the quiz is generated

    # Check if quiz has been generated
    if "quiz_manager" in st.session_state:
        quiz_manager = st.session_state["quiz_manager"]
        current_question = quiz_manager.get_question_at_index(st.session_state["question_index"])

        # Manage form and question visibility based on submission state
        if not st.session_state.get("is_submitting", False):
            with st.container():  # Display the current question and choices
                st.header(f"Question {st.session_state['question_index'] + 1}: {current_question['question']}")
                
                choices = [f"{choice['key']}) {choice['value']}" for choice in current_question["choices"]]

                # Use st.form to submit the answer
                with st.form("Multiple Choice Question"):
                    answer = st.radio("Choose the correct answer", choices)
                    submitted = st.form_submit_button("Submit")

                    if submitted:
                        # Mark as submitting to hide elements
                        st.session_state["is_submitting"] = True
                        
                        correct_answer_key = current_question['answer']
                        if answer.startswith(correct_answer_key):
                            st.success("Correct!")
                        else:
                            st.error("Incorrect!")

                        # Short delay to make transition smoother
                        time.sleep(1)

                        # Move to the next question and reset submission state
                        quiz_manager.next_question_index()
                        st.session_state["is_submitting"] = False
                        
                        # Clear the screen during submission
                        screen.empty()