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
from Quiz_Generator import QuizGenerator
from Quiz_Manager import QuizManager

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
            st.write("Let AI transform your PDFs into accurate, engaging multiple-choice quizzes, ensuring every question stays true to your document!")
            st.markdown("<br>", unsafe_allow_html=True)

            # Form to generate quiz
            with st.form("Load Data to Chroma"):
                st.subheader("⚡ Quiz Generator")
                st.write("Choose your PDFs, define the quiz topic, and click Submit to generate your quiz instantly!")

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

                    # Initialize session state for quiz
                    st.session_state["quiz_manager"] = QuizManager(question_bank)
                    st.session_state["question_index"] = 0
                    st.session_state["current_selection"] = {}  # Track the current radio selection
                    st.session_state["answers"] = {}  # Store the user-selected answers
                    st.session_state["explanations"] = {}  # Store explanations for review
                    st.session_state["feedback"] = {}  # Store feedback (Correct/Incorrect)
                    screen.empty()  # Clear the screen completely once the quiz is generated

    # Render the quiz UI if a quiz has been generated
    if "quiz_manager" in st.session_state:
        quiz_manager = st.session_state["quiz_manager"]
        question_index = st.session_state["question_index"]
        current_question = quiz_manager.get_question_at_index(question_index)

        # Retrieve previously selected answer for this question if it exists
        selected_answer = st.session_state["answers"].get(question_index, None)
        current_selection = st.session_state["current_selection"].get(question_index, selected_answer)

        st.header("📝 PDF Quizify")

        # Wrap the form logic inside the st.form context
        with st.form("Multiple Choice Question"):
            st.subheader(f"Question {question_index + 1}")

            # Display the question text
            st.write(f"Question: {current_question['question']}")

            # Retrieve the current question and choices
            choices = [f"{choice['key']}) {choice['value']}" for choice in current_question["choices"]]

            # Display radio button with the current selection
            new_selection = st.radio(
                "Choose the correct answer",
                choices,
                index=choices.index(current_selection) if current_selection else 0
            )

            # Immediate update for the current selection in session state
            st.session_state["current_selection"][question_index] = new_selection

            # If an answer is already submitted, provide feedback and explanation
            if st.session_state["answers"].get(question_index):
                selected_answer = st.session_state["answers"][question_index]
                correct_answer_key = current_question['answer']
                if selected_answer.startswith(correct_answer_key):
                    st.success("Correct!")
                else:
                    st.error("Incorrect!")
                st.write(f"Explanation: {current_question['explanation']}")

            # Layout for buttons in columns
            col1, col2, col3 = st.columns([1, 1, 1], gap="large")
            with col1:
                st.form_submit_button("⬅️ Previous Question", on_click=lambda: quiz_manager.next_question_index(direction=-1))
            with col2:
                st.form_submit_button("✔️ Submit", use_container_width=True, on_click=lambda: st.session_state["answers"].update({question_index: new_selection}))
            with col3:
                st.form_submit_button("Next Question ➡️", on_click=lambda: quiz_manager.next_question_index(direction=1))
