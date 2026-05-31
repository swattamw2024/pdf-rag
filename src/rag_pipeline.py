from src import pdf_loader, embeddings, vector_store, llm
from src.config import TOP_K


class RAGPipeline:
    def __init__(self, collection_name: str = "pdf_documents"):
        self.collection_name = collection_name

    def ingest(self, path: str) -> int:
        chunks = pdf_loader.load_and_chunk(path)
        texts = [c["text"] for c in chunks]
        embs = embeddings.embed_texts(texts)
        vector_store.add_documents(chunks, embs, self.collection_name)
        return len(chunks)

    def query(self, question: str) -> dict:
        query_emb = embeddings.embed_texts([question])[0]
        results = vector_store.query(query_emb, top_k=TOP_K, collection_name=self.collection_name)

        if not results["documents"][0]:
            return {
                "answer": "No documents have been ingested yet. Please ingest a PDF or DOCX file first.",
                "sources": [],
            }

        context_chunks = results["documents"][0]
        answer = llm.generate(question, context_chunks)

        sources = []
        for doc, meta in zip(results["documents"][0], results["metadatas"][0]):
            sources.append({
                "text": doc[:200] + "..." if len(doc) > 200 else doc,
                "source": meta["source"],
                "page": meta["page"],
            })

        return {"answer": answer, "sources": sources}

    def list_collections(self) -> list[str]:
        return vector_store.list_collections()

    def clear(self, collection_name: str | None = None):
        name = collection_name or self.collection_name
        vector_store.delete_collection(name)

    def doc_count(self) -> int:
        return vector_store.collection_count(self.collection_name)
