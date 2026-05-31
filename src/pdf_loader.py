import os
from pathlib import Path

import fitz
from docx import Document as DocxDocument
from langchain_text_splitters import RecursiveCharacterTextSplitter

from src.config import CHUNK_SIZE, CHUNK_OVERLAP

SUPPORTED_EXTENSIONS = {".pdf", ".docx"}


def extract_pdf_text(pdf_path: str) -> list[dict]:
    doc = fitz.open(pdf_path)
    pages = []
    for page_num, page in enumerate(doc, start=1):
        text = page.get_text()
        if text.strip():
            pages.append({"text": text, "page": page_num, "source": os.path.basename(pdf_path)})
    doc.close()
    return pages


def extract_docx_text(docx_path: str) -> list[dict]:
    doc = DocxDocument(docx_path)
    paragraphs = []
    current_text = []
    page_estimate = 1

    for para in doc.paragraphs:
        current_text.append(para.text)
        # Estimate ~40 lines per page for chunking metadata
        if len(current_text) >= 40:
            combined = "\n".join(current_text)
            if combined.strip():
                paragraphs.append({
                    "text": combined,
                    "page": page_estimate,
                    "source": os.path.basename(docx_path),
                })
            current_text = []
            page_estimate += 1

    if current_text:
        combined = "\n".join(current_text)
        if combined.strip():
            paragraphs.append({
                "text": combined,
                "page": page_estimate,
                "source": os.path.basename(docx_path),
            })

    return paragraphs


def extract_text(file_path: str) -> list[dict]:
    ext = Path(file_path).suffix.lower()
    if ext == ".pdf":
        return extract_pdf_text(file_path)
    if ext == ".docx":
        return extract_docx_text(file_path)
    raise ValueError(f"Unsupported file type: {ext}. Supported: {SUPPORTED_EXTENSIONS}")


def chunk_pages(pages: list[dict]) -> list[dict]:
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
        length_function=len,
    )
    chunks = []
    for page in pages:
        splits = splitter.split_text(page["text"])
        for i, text in enumerate(splits):
            chunks.append({
                "text": text,
                "source": page["source"],
                "page": page["page"],
                "chunk_index": i,
            })
    return chunks


def load_and_chunk(path: str) -> list[dict]:
    path = Path(path)
    if path.is_file() and path.suffix.lower() in SUPPORTED_EXTENSIONS:
        pages = extract_text(str(path))
        return chunk_pages(pages)

    if path.is_dir():
        all_chunks = []
        for ext in SUPPORTED_EXTENSIONS:
            for doc_file in sorted(path.glob(f"**/*{ext}")):
                pages = extract_text(str(doc_file))
                all_chunks.extend(chunk_pages(pages))
        if not all_chunks:
            raise FileNotFoundError(f"No PDF or DOCX files found in {path}")
        return all_chunks

    raise ValueError(f"Path must be a PDF/DOCX file or directory: {path}")
