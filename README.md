# RAG System with Citations and Contradiction Detection

> A production-ready Retrieval-Augmented Generation (RAG) pipeline built with FastAPI, ChromaDB, Sentence Transformers, and Groq LLM — featuring multilingual support, source citations, and document contradiction detection.

---

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Tech Stack](#tech-stack)
- [Architecture](#architecture)
- [Data Flow](#data-flow)
- [Project Structure](#project-structure)
- [Setup Guide](#setup-guide)
- [Running the Application](#running-the-application)
- [API Reference](#api-reference)
- [Evaluation](#evaluation)
- [Environment Variables](#environment-variables)
- [Knowledge Base Documents](#knowledge-base-documents)
- [Contributing](#contributing)
- [License](#license)

---

## Overview

This project is an end-to-end **Retrieval-Augmented Generation (RAG)** system that allows users to query a set of PDF documents using natural language and receive grounded, cited answers. It was built as part of an AI/ML internship at **Potens.ai**.

The system ingests academic PDFs, chunks and embeds them into a persistent ChromaDB vector store, and uses Groq's `llama-3.1-8b-instant` model to generate answers strictly from retrieved context. A Gradio web UI provides a clean interface for both Q&A and cross-document contradiction detection.

---

## Features

- **Semantic Q&A** — Ask questions in natural language and get answers grounded in your document corpus
- **Source Citations** — Every answer includes chunk-level citations with source file, chunk ID, and a text snippet
- **Confidence Scoring** — A heuristic confidence score is returned alongside each answer
- **Multilingual Support** — Questions and answers are automatically translated to/from English using `deep-translator` and `langdetect` (e.g., Hindi support)
- **Contradiction Detection** — Compare two PDF documents and get an LLM-based analysis of whether they contradict each other
- **Persistent Vector Store** — ChromaDB stores embeddings on disk so documents need not be re-indexed on every restart
- **Modular Architecture** — Clean separation of concerns across `core/`, `api/`, `store/`, `services/`, and `eval/` modules
- **Evaluation Suite** — A JSON-driven evaluation script tests system accuracy against ground-truth Q&A pairs

---

## Tech Stack

| Layer | Technology |
|---|---|
| **LLM** | Groq API (`llama-3.1-8b-instant`) |
| **Embeddings** | `sentence-transformers` (`all-MiniLM-L6-v2`) |
| **Vector Store** | ChromaDB (persistent, local) |
| **PDF Parsing** | PyMuPDF (`fitz`) |
| **Backend API** | FastAPI + Uvicorn |
| **Frontend UI** | Gradio |
| **Translation** | `deep-translator` + `langdetect` |
| **Environment** | `python-dotenv` |
| **Evaluation** | Custom Python script + JSON test cases |

---

## Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                        GRADIO FRONTEND (app.py)                 │
│          ┌──────────────────┐    ┌──────────────────────┐       │
│          │  Ask Questions   │    │ Contradiction Detection│     │
│          └────────┬─────────┘    └──────────┬────────────┘      │
└───────────────────┼─────────────────────────┼───────────────────┘
                    │ POST /ask               │ POST /contradict
                    ▼                         ▼
┌─────────────────────────────────────────────────────────────────┐
│                      FASTAPI BACKEND (run.py)                   │
│   ┌──────────────────────────┐  ┌──────────────────────────┐    │
│   │     api/ask.py           │  │   api/contradict.py       │   │
│   │  - Language detection    │  │  - PDF chunking (doc1,2)  │   │
│   │  - Translation (→EN)     │  │  - LLM contradiction      │   │
│   │  - Retrieval             │  │    analysis prompt        │   │
│   │  - LLM generation        │  └──────────────────────────┘    │
│   │  - Back-translation      │                                  │
│   │  - Citation generation   │                                  │
│   └──────────────────────────┘                                  │
└──────┬──────────────────────────────────────────────────────────┘
       │
       ▼
┌─────────────────────────────────────────────────────────────────┐
│                          CORE MODULES                           │
│                                                                 │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────────────┐   │
│  │  chunker.py  │  │ embedder.py  │  │     retriever.py     │   │
│  │  PyMuPDF     │  │ SentenceTrans│  │  embed query →       │   │
│  │  chunk_size  │  │ all-MiniLM   │  │  ChromaDB query →    │   │
│  │  =500,       │  │ L6-v2        │  │  filter & return     │   │
│  │  overlap=100 │  │              │  │  top-k chunks        │   │
│  └──────────────┘  └──────────────┘  └──────────────────────┘   │
│                                                                 │
│  ┌──────────────┐  ┌──────────────────────────────────────────┐ │
│  │   llm.py     │  │            translator.py                 │ │
│  │  Groq API    │  │  detect_language → translate_to_english  │ │
│  │  llama-3.1   │  │  → translate_from_english (back)         │ │
│  │  -8b-instant │  └──────────────────────────────────────────┘ │
│  └──────────────┘                                               │
└──────┬──────────────────────────────────────────────────────────┘
       │
       ▼
┌─────────────────────────────────────────────────────────────────┐
│                         STORAGE LAYER                           │
│                                                                 │
│   ┌─────────────────────────────────────────────────────────┐   │
│   │              store/chroma_store.py                      │   │
│   │   PersistentClient → collection: "rag_collection"       │   │
│   │   Stores: embeddings + document text + metadata         │   │
│   │   Path: data/chroma_db/                                 │   │
│   └─────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────┘
```

---

## Data Flow

### Q&A Pipeline

```
User Question (any language)
        │
        ▼
┌─────────────────────┐
│  Language Detection  │  ← langdetect
└──────────┬──────────┘
           │ non-English?
           ▼
┌─────────────────────┐
│  Translate → English │  ← deep-translator (Google)
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│  Generate Embedding  │  ← SentenceTransformer (all-MiniLM-L6-v2)
│  for the question    │      384-dimensional vector
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│  Vector Similarity   │  ← ChromaDB cosine similarity search
│  Search (top-5)      │      filters: skip chunk_id=0, len < 100
└──────────┬──────────┘
           │ retrieved_chunks
           ▼
┌─────────────────────┐
│  LLM Generation      │  ← Groq llama-3.1-8b-instant
│  (context + question)│      temperature=0 (deterministic)
└──────────┬──────────┘
           │ answer (English)
           ▼
┌─────────────────────┐
│  Back-Translate      │  ← if original question was non-English
│  Answer → original   │
│  language            │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│  Citation Generation │  ← source path, chunk_id, 350-char snippet
│  + Confidence Score  │      confidence = 0.95 - (num_citations * 0.01)
└──────────┬──────────┘
           │
           ▼
    JSON Response
  { answer, language, confidence, citations[] }
```

### Document Indexing Flow (one-time setup)

```
PDF Files (docs/)
      │
      ▼
DocumentChunker.process_pdf()
  ├── PyMuPDF: extract full text
  └── chunk_text(): size=500, overlap=100
      → List of { chunk_id, source, content }
      │
      ▼
EmbeddingGenerator.embed_chunks()
  └── SentenceTransformer.encode()
      → adds "embedding" field to each chunk
      │
      ▼
ChromaVectorStore.add_documents()
  └── chroma_collection.add(ids, embeddings, documents, metadatas)
      → persisted to data/chroma_db/
```

### Contradiction Detection Flow

```
doc1_path + doc2_path
      │
      ▼
DocumentChunker.process_pdf() × 2
  → first 3 chunks of each document
      │
      ▼
LLM Prompt:
  "Analyze whether Document 1 and Document 2 contradict each other.
   Return: Contradiction YES/NO + Reasoning"
      │
      ▼
  { doc1, doc2, analysis }
```

---

## Project Structure

```
Potens-intern-AI-ML-TanmayNalawade/
│
├── app.py                      # Gradio frontend UI (two tabs: Ask / Contradict)
├── run.py                      # FastAPI app entry point; mounts routers
├── .env                        # Environment variables (GROQ_API_KEY)
├── requirements.txt            # Full pinned dependency list
├── LICENSE                     # Project license
│
├── api/                        # FastAPI route handlers
│   ├── ask.py                  # POST /ask — full RAG pipeline with translation
│   └── contradict.py           # POST /contradict — cross-document contradiction
│
├── core/                       # Core ML/NLP logic
│   ├── chunker.py              # PDF text extraction + sliding-window chunking
│   ├── embedder.py             # Sentence embedding with all-MiniLM-L6-v2
│   ├── llm.py                  # Groq LLM wrapper (llama-3.1-8b-instant)
│   ├── retriever.py            # Embed query → ChromaDB search → filter chunks
│   └── translator.py           # Language detection + bidirectional translation
│
├── store/
│   └── chroma_store.py         # ChromaDB persistent client and collection ops
│
├── services/
│   └── citation_service.py     # Formats retrieved chunks into citation objects
│
├── data/
│   └── chroma_db/              # Persistent ChromaDB vector store (auto-created)
│       ├── chroma.sqlite3
│       └── <collection-uuid>/
│
├── docs/                       # Source PDFs (knowledge base)
│   ├── rag_paper.pdf
│   ├── transformer_paper.pdf
│   ├── chromadb_docs.pdf
│   ├── langchain_retrieval.pdf
│   └── sentence_transformers.pdf
│
├── eval/                       # Evaluation framework
│   ├── evaluate.py             # Runs questions against API, reports accuracy
│   └── questions.json          # 10 ground-truth Q&A pairs
│
├── tests/                      # Unit test directory
├── test_chroma.py              # ChromaDB integration test
├── test_chunker.py             # Chunking logic test
├── test_citation.py            # Citation service test
├── test_embedder.py            # Embedding generation test
├── test_env.py                 # Environment variable loading test
├── test_llm.py                 # LLM response test
├── test_retriever.py           # Retriever pipeline test
└── test_translator.py          # Translation service test
```

---

## Setup Guide

### Prerequisites

- Python 3.10 or higher
- A [Groq API key](https://console.groq.com/) (free tier available)
- Git

### 1. Clone the Repository

```bash
git clone https://github.com/<your-username>/Potens-intern-AI-ML-TanmayNalawade.git
cd Potens-intern-AI-ML-TanmayNalawade
```

### 2. Create and Activate a Virtual Environment

```bash
# Create virtual environment
python -m venv venv

# Activate (Linux/macOS)
source venv/bin/activate

# Activate (Windows)
venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

> **Note:** The requirements file is a full pip freeze. Key packages installed include: `fastapi`, `uvicorn`, `gradio`, `chromadb`, `sentence-transformers`, `groq`, `PyMuPDF`, `deep-translator`, `langdetect`, `python-dotenv`.

### 4. Configure Environment Variables

Create a `.env` file in the project root:

```bash
cp .env.example .env   # if example exists, otherwise create manually
```

Edit `.env` and add your Groq API key:

```env
GROQ_API_KEY=your_groq_api_key_here
```

> **Never commit your `.env` file.** Ensure `.env` is listed in your `.gitignore`.

### 5. Index the Documents

Before querying, the PDF documents must be chunked, embedded, and stored in ChromaDB. Run the indexing script (or the relevant test) to populate the vector store:

```bash
python test_chroma.py
```

This reads PDFs from `docs/`, generates embeddings, and persists them to `data/chroma_db/`. This step only needs to be run once (or whenever new documents are added).

---

## Running the Application

The system has two components that must be run simultaneously: the **FastAPI backend** and the **Gradio frontend**.

### Terminal 1 — Start the FastAPI Backend

```bash
uvicorn run:app --host 127.0.0.1 --port 8000 --reload
```

The API will be available at `http://127.0.0.1:8000`. You can explore the auto-generated docs at `http://127.0.0.1:8000/docs`.

### Terminal 2 — Start the Gradio Frontend

```bash
python app.py
```

Gradio will launch in your browser automatically. If not, navigate to `http://127.0.0.1:7860`.

---

## API Reference

### `POST /ask`

Ask a question against the indexed document corpus.

**Request Body:**
```json
{
  "question": "What is Retrieval-Augmented Generation?"
}
```

**Response:**
```json
{
  "question": "What is Retrieval-Augmented Generation?",
  "language": "en",
  "answer": "Retrieval-Augmented Generation (RAG) is a technique that...",
  "confidence": 0.93,
  "citations": [
    {
      "source": "docs/rag_paper.pdf",
      "chunk_id": 4,
      "snippet": "RAG combines a retrieval component with a generative model..."
    }
  ]
}
```

**Multilingual Example:**
```json
{
  "question": "रिट्रीवल ऑगमेंटेड जनरेशन क्या है?"
}
```
The system detects Hindi (`hi`), translates the question to English, retrieves context, generates an answer, and translates the response back to Hindi before returning.

---

### `POST /contradict`

Analyze two PDF documents for logical contradictions.

**Request Body:**
```json
{
  "doc1": "docs/rag_paper.pdf",
  "doc2": "docs/transformer_paper.pdf"
}
```

**Response:**
```json
{
  "doc1": "docs/rag_paper.pdf",
  "doc2": "docs/transformer_paper.pdf",
  "analysis": "Contradiction: NO\n\nReasoning: Both documents are complementary..."
}
```

---

## Evaluation

An automated evaluation suite is included to measure system performance against a set of predefined questions with expected answers.

### Running the Evaluation

Ensure the FastAPI backend is running, then:

```bash
python eval/evaluate.py
```

### Sample Questions in `eval/questions.json`

- What is Retrieval-Augmented Generation?
- What problem does RAG solve?
- What is the Transformer architecture?
- What does the Transformer remove compared to older models?
- What is self-attention in Transformers?
- What is ChromaDB used for?
- What are embeddings in RAG systems?
- Why is chunk overlap important?
- What is semantic retrieval?
- Why are citations important in RAG systems?

### Evaluation Output

The script prints per-question results including predicted answer, ground truth, confidence score, and pass/fail status. At the end it reports:

```
FINAL EVALUATION RESULTS
Total Questions: 10
Successful Answers: X
Approx Accuracy: XX.XX%
```

A question is considered successful if the LLM did not respond with `"I could not find the answer in the provided documents."`.

---

## Environment Variables

| Variable | Description | Required |
|---|---|---|
| `GROQ_API_KEY` | API key for Groq cloud inference | ✅ Yes |

---

## Knowledge Base Documents

The `docs/` directory contains the five academic PDFs that form the system's knowledge base:

| File | Description |
|---|---|
| `rag_paper.pdf` | Original RAG paper — retrieval-augmented generation for NLP |
| `transformer_paper.pdf` | "Attention Is All You Need" — Transformer architecture |
| `chromadb_docs.pdf` | ChromaDB documentation — vector storage and retrieval |
| `langchain_retrieval.pdf` | LangChain retrieval concepts and architecture |
| `sentence_transformers.pdf` | Sentence-BERT and sentence embedding techniques |

To add new documents, place them in `docs/` and re-run the indexing step.

---

## Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/your-feature-name`
3. Make your changes with clear, focused commits
4. Run the test scripts to verify nothing is broken
5. Open a pull request with a description of your changes

---

## License

This project is licensed under the terms specified in the [LICENSE](LICENSE) file.

---

*Built by Tanmay Nalawade — AI/ML Intern at Potens.ai*
