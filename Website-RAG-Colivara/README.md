# MultiModal RAG with ColiVara and DeepSeek-Janus-Pro

This project implements a MultiModal RAG with DeepSeek's latest model Janus-Pro and ColiVara.

We use the following tools
- DeepSeek-Janus-Pro as the multi-modal LLM.
- [ColiVara](https://colivara.com/) for SOTA document understanding and retrieval.
- [Firecrawl](https://www.firecrawl.dev/i/api) for web scraping.
- Streamlit as the web interface.

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

**Get the API keys**:
- [ColiVara](https://colivara.com/) for SOTA document understanding and retrieval.
- [Firecrawl](https://www.firecrawl.dev/i/api) for web scraping.

Create a .env file and store them as follows:
```python
COLIVARA_API_KEY="<COLIVARA-API-KEY>"
FIRECRAWL_API_KEY="<FIRECRAWL-API-KEY>"
```


**Install Dependencies**:
   Ensure you have Python 3.11 or later installed.
   ```bash
   pip install streamlit-pdf-viewer colivara-py streamlit fastembed flash-attn transformers
   ```

---

## Run the project

Finally, run the project by running the following command:

```bash
streamlit run app.py
```


---

