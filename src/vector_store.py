import hashlib

import chromadb

from src.config import CHROMA_DB_PATH, DEFAULT_COLLECTION


def get_client() -> chromadb.PersistentClient:
    return chromadb.PersistentClient(path=CHROMA_DB_PATH)


def get_collection(name: str = DEFAULT_COLLECTION) -> chromadb.Collection:
    client = get_client()
    return client.get_or_create_collection(name=name, metadata={"hnsw:space": "cosine"})


def add_documents(chunks: list[dict], embeddings: list[list[float]], collection_name: str = DEFAULT_COLLECTION):
    collection = get_collection(collection_name)
    ids = []
    documents = []
    metadatas = []
    for chunk in chunks:
        chunk_id = hashlib.md5(f"{chunk['source']}:{chunk['page']}:{chunk['chunk_index']}".encode()).hexdigest()
        ids.append(chunk_id)
        documents.append(chunk["text"])
        metadatas.append({"source": chunk["source"], "page": chunk["page"], "chunk_index": chunk["chunk_index"]})

    batch_size = 500
    for i in range(0, len(ids), batch_size):
        collection.upsert(
            ids=ids[i:i + batch_size],
            embeddings=embeddings[i:i + batch_size],
            documents=documents[i:i + batch_size],
            metadatas=metadatas[i:i + batch_size],
        )


def query(query_embedding: list[float], top_k: int = 5, collection_name: str = DEFAULT_COLLECTION) -> dict:
    collection = get_collection(collection_name)
    if collection.count() == 0:
        return {"documents": [[]], "metadatas": [[]], "distances": [[]]}
    return collection.query(query_embeddings=[query_embedding], n_results=min(top_k, collection.count()))


def list_collections() -> list[str]:
    client = get_client()
    return [c.name for c in client.list_collections()]


def delete_collection(name: str):
    client = get_client()
    client.delete_collection(name)


def collection_count(name: str = DEFAULT_COLLECTION) -> int:
    return get_collection(name).count()
