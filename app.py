import os
import requests
from fastapi import FastAPI
from pydantic import BaseModel

from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings, ChatOpenAI


# =========================
# BASIC SETUP
# =========================

os.environ["OPENAI_API_KEY"] = "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"

app = FastAPI()

# This will store the vector database after ingestion
vector_db = None


# =========================
# REQUEST MODELS
# =========================

class IngestRequest(BaseModel):
    link: str   # Google Doc link


class ChatRequest(BaseModel):
    query: str  # User question


# =========================
# HELPER FUNCTIONS
# =========================

def fetch_google_doc_text(doc_link: str) -> str:
    """
    Fetch text from a PUBLIC Google Doc using TXT export.
    """
    if "/d/" not in doc_link:
        return ""

    doc_id = doc_link.split("/d/")[1].split("/")[0]
    url = f"https://docs.google.com/document/d/{doc_id}/export?format=txt"

    response = requests.get(url)
    if response.status_code != 200:
        return ""

    return response.text


def split_text_simple(text, chunk_size=800, overlap=100):
    """
    Simple text splitter.
    Beginner-friendly and dependency-free.
    """
    chunks = []
    start = 0

    while start < len(text):
        end = start + chunk_size
        chunk = text[start:end]
        chunks.append(chunk)
        start = end - overlap

    return chunks


# =========================
# ROOT ENDPOINT
# =========================

@app.get("/")
def root():
    return {
        "status": "ok",
        "message": "RAG API is running. Open /docs for Swagger UI."
    }


# =========================
# INGEST ENDPOINT
# =========================

@app.post("/ingest")
def ingest_document(request: IngestRequest):
    """
    1. Fetch Google Doc text
    2. Split into chunks
    3. Create embeddings
    4. Store in vector database
    """
    global vector_db

    document_text = fetch_google_doc_text(request.link)

    if not document_text.strip():
        return {"error": "Document is empty or not public"}

    chunks = split_text_simple(document_text)

    vector_db = Chroma.from_texts(
        chunks,
        OpenAIEmbeddings()
    )

    return {
        "message": "Document ingested successfully",
        "total_chunks": len(chunks)
    }


# =========================
# CHAT ENDPOINT
# =========================

@app.post("/chat")
def chat_with_document(request: ChatRequest):
    """
    Answer questions ONLY using document content.
    """
    if vector_db is None:
        return {"error": "Please ingest a document first"}

    docs = vector_db.similarity_search(request.query, k=3)

    if not docs:
        return {"answer": "This information is not in the document."}

    context = ""
    for i, doc in enumerate(docs):
        context += f"(Section {i+1}) {doc.page_content}\n\n"

    prompt = f"""
Answer the question using ONLY the context below.
If the answer is not present, say:
"This information is not in the document."

Context:
{context}

Question: {request.query}

Answer with citations like (Section 1).
"""

    llm = ChatOpenAI(model="gpt-4o-mini")
    answer = llm.predict(prompt)

    return {"answer": answer}
