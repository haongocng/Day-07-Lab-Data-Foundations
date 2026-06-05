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
        """Initialize the agent with a vector store and LLM function."""
        self.store = store
        self.llm_fn = llm_fn

    def answer(self, question: str, top_k: int = 3) -> str:
        """
        Answer a question using RAG (Retrieval-Augmented Generation).

        Steps:
        1. Retrieve top-k most relevant chunks from the knowledge base
        2. Build a prompt with retrieved context
        3. Call LLM to generate an answer based on context
        """
        # Step 1: Retrieve relevant chunks
        results = self.store.search(question, top_k=top_k)

        # Step 2: Build context from retrieved chunks
        if not results:
            context = "No relevant information found in the knowledge base."
        else:
            context_parts = []
            for i, result in enumerate(results, 1):
                context_parts.append(f"[{i}] {result['content']}")
            context = "\n".join(context_parts)

        # Step 3: Build prompt for LLM
        prompt = f"""Based on the following context, please answer the question.

Context:
{context}

Question: {question}

Answer:"""

        # Step 4: Call LLM to generate answer
        answer = self.llm_fn(prompt)

        return answer
