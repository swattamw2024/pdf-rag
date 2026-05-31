import tempfile
from pathlib import Path

import streamlit as st

from src.rag_pipeline import RAGPipeline

st.set_page_config(page_title="PDF RAG", page_icon="📄", layout="wide")


def get_pipeline() -> RAGPipeline:
    collection = st.session_state.get("collection_name", "pdf_documents")
    return RAGPipeline(collection_name=collection)


# --- Sidebar ---
with st.sidebar:
    st.header("Document Manager")

    st.text_input("Collection name", value="pdf_documents", key="collection_name")

    uploaded_files = st.file_uploader(
        "Upload PDF or DOCX files",
        type=["pdf", "docx"],
        accept_multiple_files=True,
    )

    if st.button("Ingest", disabled=not uploaded_files):
        pipeline = get_pipeline()
        total_chunks = 0
        progress = st.progress(0)

        for i, uploaded in enumerate(uploaded_files):
            suffix = Path(uploaded.name).suffix
            with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
                tmp.write(uploaded.read())
                tmp_path = tmp.name

            with st.spinner(f"Processing {uploaded.name}..."):
                count = pipeline.ingest(tmp_path)
                total_chunks += count

            Path(tmp_path).unlink(missing_ok=True)
            progress.progress((i + 1) / len(uploaded_files))

        st.success(f"Ingested {len(uploaded_files)} file(s) — {total_chunks} chunks indexed.")

    st.divider()

    pipeline = get_pipeline()
    collections = pipeline.list_collections()
    if collections:
        st.subheader("Collections")
        for name in collections:
            st.text(f"• {name}")
    else:
        st.info("No collections yet. Upload and ingest documents to get started.")

    st.divider()
    st.caption("Runs fully offline with Ollama + ChromaDB")


# --- Chat interface ---
st.title("📄 PDF RAG — Ask Your Documents")

if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])
        if msg.get("sources"):
            with st.expander("Sources"):
                for s in msg["sources"]:
                    st.markdown(f"**{s['source']}** (page {s['page']})")
                    st.caption(s["text"])

if prompt := st.chat_input("Ask a question about your documents..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            pipeline = get_pipeline()
            result = pipeline.query(prompt)

        st.markdown(result["answer"])
        if result["sources"]:
            with st.expander("Sources"):
                for s in result["sources"]:
                    st.markdown(f"**{s['source']}** (page {s['page']})")
                    st.caption(s["text"])

        st.session_state.messages.append({
            "role": "assistant",
            "content": result["answer"],
            "sources": result["sources"],
        })
