# 📈 FinSight AI

A production-ready Multi-Agent Financial Intelligence Platform built with FastAPI, Streamlit, LangGraph, Hybrid RAG, ChromaDB, Ollama, and Model Context Protocol (MCP).

FinSight AI helps investors, analysts, and researchers analyze companies, earnings transcripts, portfolios, and cross-company strategic trends using AI-powered financial intelligence workflows and production-ready AI tools.

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

---

### 🔌 MCP (Model Context Protocol)

FinSight AI exposes its AI capabilities as production-ready MCP tools, enabling AI assistants like Claude Desktop and Cursor to access financial intelligence workflows.

Available MCP Tools:

- Company Analysis
- Company Comparison
- Portfolio Analysis
- News Analysis
- Financial Metrics Analysis
- Earnings PDF Indexing
- Earnings Q&A (RAG)
- Transcript Summarization
- Multi-Transcript Analysis

Supports:

- FastMCP
- Tool Calling
- Local AI Workflows
- AI Assistant Integration

---

## 🧠 AI Architecture

FinSight AI uses a multi-agent architecture powered by LangGraph.

### AI Agents

- Company Analysis Agent
- Metrics Analysis Agent
- News Analysis Agent
- Risk Analysis Agent
- Investment Analysis Agent
- Portfolio Analysis Agent
- Earnings Analysis Agent
- Earnings RAG Agent
- Transcript Summary Agent
- Multi-Transcript Intelligence Agent

### Workflow

- LangGraph Multi-Agent Orchestration
- Stateful Financial Analysis Pipeline
- Hybrid Retrieval Pipeline
- MCP Tool Layer

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

### AI Infrastructure

- FastMCP
- Model Context Protocol (MCP)
- Hybrid Retrieval
- Cross-Encoder Reranking

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
├── mcp/
├── prompts/
├── rag/
├── services/

frontend/
└── streamlit_app.py

tests/

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

## ▶️ Run MCP Server

```bash
python -m app.mcp.server

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

- Multi-Agent AI Architecture
- LangGraph Workflow Orchestration
- Production-Ready MCP Server
- FastMCP Tool Integration
- Hybrid RAG Pipeline
- Multi-Document Financial Intelligence
- Cross-Transcript Analysis
- Query Expansion
- BM25 + Vector Retrieval
- Cross-Encoder Reranking
- Local LLM Inference (Ollama)
- Financial Research Automation
- Source-Grounded Answers
