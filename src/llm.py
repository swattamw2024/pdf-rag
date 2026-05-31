import ollama

from src.config import OLLAMA_MODEL

RAG_PROMPT_TEMPLATE = """You are a helpful assistant. Answer the question based ONLY on the provided context.
If the answer is not in the context, say "I don't have enough information to answer that."

Context:
{context}

Question: {question}

Answer:"""


def generate(question: str, context_chunks: list[str]) -> str:
    context = "\n\n---\n\n".join(context_chunks)
    prompt = RAG_PROMPT_TEMPLATE.format(context=context, question=question)

    try:
        response = ollama.chat(
            model=OLLAMA_MODEL,
            messages=[{"role": "user", "content": prompt}],
        )
        return response["message"]["content"]
    except Exception as e:
        if "connection" in str(e).lower() or "refused" in str(e).lower():
            raise ConnectionError(
                "Cannot connect to Ollama. Make sure it's running with: ollama serve"
            ) from e
        raise
