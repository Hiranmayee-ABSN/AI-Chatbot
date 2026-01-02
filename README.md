# Google Doc RAG Chatbot

## Problem Statement
Build an AI chatbot that reads data from a Google Document and answers user questions
strictly based on the document content using Retrieval-Augmented Generation (RAG).

---

## Overview
This project implements a simple RAG-based chatbot using FastAPI.
The chatbot ingests a **publicly shared Google Doc**, converts it into semantic chunks,
stores them in a vector database, and retrieves the most relevant sections to answer
user questions.

The system avoids hallucinations by responding only with information present in the
document.

---

## Features
- Public Google Doc ingestion (no manual copy-paste)
- Automatic text chunking
- Vector similarity search using ChromaDB
- Context-aware question answering
- Graceful handling of out-of-scope questions
- Simple API interface via Swagger UI

---

## Tech Stack
- Python
- FastAPI
- LangChain
- ChromaDB
- Requests

---

## Project Structure
```

rag-google-doc-chatbot/
│
├── app.py
├── requirements.txt
└── README.md

````

---

## Setup Instructions

### 1. Install Dependencies
```bash
pip install -r requirements.txt
````

### 2. Run the Server

```bash
uvicorn app:app --reload
```

### 3. Open API Docs

```
http://127.0.0.1:8000/docs
```

---

## API Endpoints

### POST `/ingest`

Ingests a publicly shared Google Document.

**Request Body:**

```json
{
  "link": "https://docs.google.com/document/d/XXXX/edit"
}
```

---

### POST `/chat`

Asks a question based on the ingested document.

**Request Body:**

```json
{
  "query": "What is the purpose of this document?"
}
```

---

## Example Workflow

1. Open Swagger UI
2. Ingest a public Google Doc
3. Ask multiple questions
4. Receive answers based only on document content
5. Ask an unrelated question to see fallback response

---

## Edge Case Handling

* Empty or private documents are rejected
* Out-of-scope questions return:

  > "This information is not in the document."

---

## Notes

This project is designed as a **beginner-friendly demonstration** of
Retrieval-Augmented Generation concepts and can be extended with larger documents,
advanced ranking, or UI enhancements.

---
# Demo Screenshots
<img width="1832" height="968" alt="image" src="https://github.com/user-attachments/assets/b0c74651-6248-490e-82cc-f3fe18cca96f" />

