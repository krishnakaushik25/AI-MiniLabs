# **📝 PDF Quizify**

**PDF Quizify: AI-Driven Quiz Builder**

PDF Quizify is an AI-powered tool that automatically generates multiple-choice quizzes from user-uploaded PDFs. It leverages **Google Vertex AI**, a machine learning platform, to process the data. Specifically, **textembedding-gecko@003**, a model within **Vertex AI**, converts the document text into embeddings. These embeddings are then passed to **Google Gemini**, also part of **Vertex AI**, to generate questions and answers, ensuring the quiz remains true to the source content. The results are returned in a structured JSON format using **Structured Output Parsing**, which is displayed through an interactive interface built with **Streamlit**.

The project also incorporates:
- **Google Service Account** for authentication
- **Langchain** for structured output parsing
- **Chroma** for embedding persistence

---

## **How It Works**

**PDF Quizify** uses a combination of AI models and machine learning technologies offered by **Google Vertex AI** to turn PDFs into interactive multiple-choice quizzes. Here’s a detailed breakdown:

1. **Document Ingestion**:
   - Users upload PDFs through the **Streamlit** interface.
   - A **PDF Loader** extracts the text from the uploaded files, which is used as the basis for further processing.

2. **Embedding Generation**:
   - The extracted text is processed into embeddings using the **textembedding-gecko@003** model, part of the **Vertex AI** platform. These embeddings represent the semantic structure and meaning of the text, enabling more intelligent question generation.

3. **Embedding Persistence with Chroma**:
   - The generated embeddings are stored in **Chroma**, a persistence layer that ensures the data is saved for future use without requiring reprocessing of the PDF.

4. **Question and Answer Generation with Google Gemini**:
   - After the embeddings are created, the processed data is sent to **Google Gemini**, a large language model (LLM) within **Vertex AI**. **Gemini** analyzes the embeddings and generates quiz questions, multiple-choice answers, and explanations.
   - To ensure the response is structured consistently, **Structured Output Parsing** is used. This involves defining the output schema to ensure **Gemini** returns the questions, answers, and explanations in JSON format.

5. **Structured Output Parsing with Langchain**:
   - **Langchain** is used to parse the structured output from **Google Gemini** and prepare it for display in the user interface. This ensures that the questions and answers are properly formatted for the quiz interface.

6. **Interactive User Interface with Streamlit**:
   - The JSON-formatted quiz data is displayed through the **Streamlit** interface, where users can:
     - Navigate through the quiz questions
     - Select answers
     - Submit their responses and receive immediate feedback
   - The feedback includes whether the answer was correct and provides an explanation, enhancing the learning experience.

7. **Authentication with Google Service Account**:
   - Access to **Vertex AI** and its models, including **textembedding-gecko@003** and **Google Gemini**, is handled securely using a **Google Service Account**.

### **Summary of the Workflow**:
- PDFs are uploaded and their text is extracted.
- The extracted text is embedded using **textembedding-gecko@003** via **Vertex AI**.
- The embeddings are stored in **Chroma** for future use.
- **Google Gemini**, within **Vertex AI**, generates quiz questions, answers, and explanations, which are returned in JSON format using **Structured Output Parsing**.
- **Langchain** ensures the JSON output is properly parsed and formatted for display.
- The quiz is presented in a **Streamlit** interface, where users interact with questions and receive feedback.
- Secure access to **Vertex AI** is managed via a **Google Service Account**.

---

## **Program Structure**

### **Embedding Client**
![image](https://github.com/user-attachments/assets/f3a980f2-5898-43dc-aa50-1bdc5f7a4b81)

### **Document Ingestion**
![image](https://github.com/user-attachments/assets/e116e08b-f332-4606-8f45-d0d9071577a6)

### **Quiz Generation**
![image](https://github.com/user-attachments/assets/71be70e1-7587-4e16-8199-1dc63444d936)

### **Generate Quiz Algorithm**
![image](https://github.com/user-attachments/assets/2c06697e-bc7e-47d0-b87f-f388e51d9b59)

### **Screen State Handling**
![image](https://github.com/user-attachments/assets/a3176261-21de-4586-8ae6-88c7cf55f59a)

### **Question Layout (in JSON)**
![image](https://github.com/user-attachments/assets/27d6a590-1217-4d78-8f9c-ca1cda2d26d3)



## **Screenshots**
![Screenshot 2024-09-12 015323](https://github.com/user-attachments/assets/e6c9cb9f-107f-42e2-9ff7-5722fe967eab)

![Screenshot 2024-09-12 020923](https://github.com/user-attachments/assets/91e4d12b-bdb8-4df4-b46c-6df87fea9bc9)

![Screenshot 2024-09-12 020937](https://github.com/user-attachments/assets/80e114cc-19e7-4de4-b3a7-d031809fe9b5)
