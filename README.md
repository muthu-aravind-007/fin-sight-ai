# 📈 FinSight AI

AI-Powered Financial Intelligence Platform built with FastAPI, Streamlit, LangGraph, Hybrid RAG, ChromaDB, and Ollama.

FinSight AI helps investors, analysts, and researchers analyze companies, earnings transcripts, portfolios, and cross-company strategic trends using AI-powered financial intelligence workflows.

---

## 🚀 Features

### 📈 Company Analysis

Analyze a public company using its stock ticker.

Includes:

* Company overview
* Market capitalization
* P/E ratio
* Growth analysis
* Risk analysis
* News sentiment analysis
* AI-generated business insights

---

### ⚔️ Company Comparison

Compare two companies side-by-side.

Includes:

* Revenue comparison
* Market cap comparison
* Growth comparison
* Risk comparison
* AI-generated competitive analysis

Example:

* NVIDIA vs AMD
* Microsoft vs Google
* Apple vs Samsung

---

### 📄 Earnings Call Analyzer

Analyze raw earnings call transcripts.

Extracts:

* Strategic priorities
* Growth opportunities
* Business risks
* Market trends
* Management commentary

---

### 📊 Portfolio Analyzer

Analyze a portfolio of stocks.

Includes:

* Portfolio score
* Diversification analysis
* Sector allocation
* AI-generated portfolio insights

---

### 🤖 Earnings Q&A (RAG)

Upload a single earnings transcript PDF and ask questions.

Examples:

* What are the key risks?
* What drove revenue growth?
* What did management say about AI demand?
* What is the future outlook?

Uses Retrieval-Augmented Generation (RAG) to provide source-backed answers.

---

### 📚 Multi-Transcript Intelligence

Upload multiple earnings transcripts and perform cross-company analysis.

Examples:

* Compare Microsoft vs NVIDIA AI strategy
* Compare cloud infrastructure investments
* Compare management outlook across quarters
* Identify common growth drivers

Supports:

* Multi-document retrieval
* Company-aware filtering
* Quarter-aware filtering
* Cross-company reasoning

---

## 🧠 AI Architecture

FinSight AI uses a multi-agent architecture powered by LangGraph.

### Agents

* Company Analysis Agent
* News Analysis Agent
* Risk Analysis Agent
* Portfolio Analysis Agent
* Earnings Analysis Agent
* Earnings RAG Agent
* Multi-Transcript RAG Agent

---

## 🔍 Hybrid RAG Pipeline

The transcript intelligence system uses:

### Retrieval

* ChromaDB Vector Search
* BM25 Keyword Search
* Query Expansion
* Metadata Filtering

### Ranking

* BGE Embeddings
* BGE Reranker

### Generation

* Qwen 2.5 7B
* Ollama Local Inference

---

## 🏗️ Tech Stack

### Frontend

* Streamlit

### Backend

* FastAPI

### AI / LLM

* Ollama
* Qwen 2.5 7B
* LangGraph

### RAG

* ChromaDB
* Sentence Transformers
* BM25
* BGE Embeddings
* BGE Reranker

### Data

* Yahoo Finance
* Earnings Transcripts (PDF)

---

## 📂 Project Structure

```text
app/
├── agents/
├── api/
├── graph/
├── models/
├── prompts/
├── rag/
├── services/

frontend/
└── streamlit_app.py

tests/
```

## ⚙️ Installation

### Clone Repository

```bash
git clone https://github.com/muthu-aravind-007/fin-sight-ai.git

cd fin-sight-ai
```

### Create Virtual Environment

```bash
python -m venv venv

venv\Scripts\activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Install Ollama

Download:

https://ollama.com

Pull Qwen Model:

```bash
ollama pull qwen2.5:7b
```

Start Ollama:

```bash
ollama serve
```

---

## ▶️ Run Backend

```bash
uvicorn app.main:app --reload
```

Backend:

```text
http://localhost:8000
```

---

## ▶️ Run Frontend

```bash
streamlit run frontend/streamlit_app.py
```

Frontend:

```text
http://localhost:8501
```

---

## 📊 Example Use Cases

### Financial Research

* Analyze earnings transcripts
* Compare competitors
* Track AI strategy across companies

### Investment Research

* Portfolio analysis
* Company risk assessment
* Growth opportunity identification

### AI-Powered Business Intelligence

* Cross-company transcript analysis
* Strategic trend discovery
* Competitive intelligence

---

## 🔮 Future Improvements

* SEC Filing Analysis (10-K / 10-Q)
* Real-Time Market Intelligence
* Multi-Agent Planning Workflows
* Cloud Deployment
* Watchlists & Alerts
* Enterprise Research Dashboard

---

## 👨‍💻 Author

Aravind

B.Tech Computer Science Engineering (AI & ML)

GitHub:
https://github.com/muthu-aravind-007

---

## ⭐ Key Highlights

* Multi-Agent AI Architecture
* LangGraph Workflow Orchestration
* Hybrid RAG System
* Cross-Transcript Intelligence
* Local LLM Inference with Ollama
* Financial Research Automation
* Source-Grounded Answers
