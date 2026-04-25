# 🧠 Intelligent Business Document Analyzer

> Upload any business PDF and query it in natural language — powered by RAG (Retrieval Augmented Generation)

![Python](https://img.shields.io/badge/Python-3.11-blue?logo=python)
![FastAPI](https://img.shields.io/badge/FastAPI-0.110-009688?logo=fastapi)
![Streamlit](https://img.shields.io/badge/Streamlit-1.32-FF4B4B?logo=streamlit)
![Docker](https://img.shields.io/badge/Docker-Containerized-2496ED?logo=docker)
![LangChain](https://img.shields.io/badge/LangChain-LCEL-000000)
![ChromaDB](https://img.shields.io/badge/ChromaDB-VectorStore-orange)
![Groq](https://img.shields.io/badge/Groq-LLaMA3.3--70B-blueviolet)

### 🚀 [Try the Live Demo on Hugging Face Spaces](https://huggingface.co/spaces/Adeelkamal/Intelligent-Business-Document-Analyzer)

---

## 🚀 What It Does

This app lets you upload any business document (annual reports, contracts, research papers, financial statements) and ask questions about it in plain English. The system finds the most relevant sections and generates a precise answer with **page citations**.

**Example:**
> *"What was the company's net revenue in 2024?"*
> *"What are the key risk factors mentioned?"*
> *"Summarize the executive strategy section."*

---

## 🏗️ Architecture

```
User uploads PDF
      ↓
[Streamlit Frontend] → POST /upload → [FastAPI Backend]
                                             ↓
                                      PyMuPDF reads PDF
                                             ↓
                                   Split into text chunks
                                             ↓
                              HuggingFace Embeddings (all-MiniLM-L6-v2)
                                             ↓
                                   Stored in ChromaDB

User asks question
      ↓
[Streamlit Frontend] → POST /query → [FastAPI Backend]
                                             ↓
                              ChromaDB similarity search (top 15 chunks)
                                             ↓
                              Groq LLaMA 3.3-70B generates answer
                                             ↓
                         Answer + page citations returned to user
```

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| Frontend | Streamlit |
| Backend | FastAPI + Uvicorn |
| LLM | Groq — LLaMA 3.3 70B Versatile |
| Embeddings | HuggingFace all-MiniLM-L6-v2 |
| Vector Store | ChromaDB |
| PDF Parsing | PyMuPDF (pymupdf) |
| Orchestration | LangChain LCEL |
| Containerization | Docker + Docker Compose |

---

## ⚙️ Run Locally

### Prerequisites
- Docker Desktop installed and running
- Groq API key → [console.groq.com](https://console.groq.com)

### Steps

**1. Clone the repo**
```bash
git clone https://github.com/Adeel-lab/Intelligent-Business-Document-Analyzer.git
cd Intelligent-Business-Document-Analyzer
```

**2. Create your `.env` file**
```bash
GROQ_API_KEY=your_groq_api_key_here
```

**3. Build and run with Docker**
```bash
docker compose up --build
```

**4. Open the app**
- Streamlit UI → http://localhost:8501
- FastAPI docs → http://localhost:8000/docs

---

## 📁 Project Structure

```
├── app.py              # Streamlit frontend
├── main.py             # FastAPI backend (REST API)
├── ingest.py           # PDF loading, chunking, embedding
├── retriever.py        # RAG chain — ChromaDB + Groq LLM
├── requirements.txt    # Python dependencies
├── Dockerfile          # Container configuration
├── docker-compose.yaml # Multi-container orchestration
└── .env                # API keys (not committed)
```

---

## 👤 Author

**Adeel Kamal**
- 🔗 [LinkedIn](https://www.linkedin.com/in/adeel-kamal-8231b4295)
- 🐙 [GitHub](https://github.com/Adeel-lab)

---

## 📄 License

MIT License — free to use and modify.
