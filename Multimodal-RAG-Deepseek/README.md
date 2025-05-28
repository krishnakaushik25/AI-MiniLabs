# MultiModal RAG with DeepSeek-Janus-Pro

This project implements a MultiModal RAG with DeepSeek's latest model Janus-Pro.

We use the following tools
- DeepSeek-Janus-Pro as the multi-modal LLM
- ColPali as the vision encoder
- Qdrant as the vector database
- Streamlit as the web interface

## Demo

A demo of the project is available below:

![demo](./video-demo.mp4)

---
## Setup and installations

**Setup Janus**:
```
git clone https://github.com/deepseek-ai/Janus.git
pip install -e ./Janus
```

**Install Dependencies**:
   Ensure you have Python 3.11 or later installed.
   ```bash
   pip install streamlit fastembed flash-attn transformers
   ```

---

## Run the project

Finally, run the project by running the following command:

```bash
streamlit run app.py
```


---
