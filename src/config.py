import os

OLLAMA_MODEL = os.getenv("PDF_RAG_MODEL", "llama3.2")
EMBEDDING_MODEL = "all-MiniLM-L6-v2"

CHUNK_SIZE = 1000
CHUNK_OVERLAP = 200

CHROMA_DB_PATH = os.getenv("PDF_RAG_DB_PATH", "./data/chroma_db")
DEFAULT_COLLECTION = "pdf_documents"

TOP_K = 5
