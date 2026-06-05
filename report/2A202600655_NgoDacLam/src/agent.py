from typing import Callable

from .store import EmbeddingStore


class KnowledgeBaseAgent:
    """
    An agent that answers questions using a vector knowledge base.

    Retrieval-augmented generation (RAG) pattern:
        1. Retrieve top-k relevant chunks from the store.
        2. Build a prompt with the chunks as context.
        3. Call the LLM to generate an answer.
    """

    def __init__(self, store: EmbeddingStore, llm_fn: Callable[[str], str]) -> None:
        self.store = store
        self.llm_fn = llm_fn

    def answer(self, question: str, top_k: int = 3) -> str:
        results = self.store.search(question, top_k=top_k)
        context_lines: list[str] = []
        for index, result in enumerate(results, start=1):
            source = result["metadata"].get("source", "unknown")
            context_lines.append(f"Source {index}: {source}\n{result['content']}")
        context_text = "\n\n".join(context_lines).strip()
        prompt = (
            "Use the following retrieved context to answer the question.\n\n"
            f"{context_text}\n\nQuestion: {question}"
        )
        return self.llm_fn(prompt)
