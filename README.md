# Google Doc RAG Chatbot

## Overview
This project is a beginner-friendly Retrieval-Augmented Generation (RAG) chatbot.
It ingests a publicly shared Google Document and answers user questions strictly
based on the document content.

The system avoids hallucinations by retrieving exact document sections instead of
generating unsupported answers.

## Features
- Google Doc ingestion via public link
- Automatic text chunking
- Semantic search using ChromaDB
- Context-based answers
- Graceful handling of out-of-scope questions

## Tech Stack
- Python
- FastAPI
- LangChain
- ChromaDB

## How to Run Locally
```bash
pip install -r requirements.txt
uvicorn app:app --reload
