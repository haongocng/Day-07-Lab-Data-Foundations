"""
Demo RAG System with Real LLM

This demo shows how to use the KnowledgeBaseAgent with a real LLM endpoint.
Uses environment variables for configuration.
"""

import os
import requests
from dotenv import load_dotenv
from agent import KnowledgeBaseAgent
from store import EmbeddingStore
from models import Document

# Load environment variables from .env file
load_dotenv()

# LLM Configuration from environment
LLM_API_BASE = os.getenv("LLM_API_BASE", "http://localhost:20128/v1")
LLM_API_KEY = os.getenv("LLM_API_KEY", "")
LLM_MODEL = os.getenv("LLM_MODEL", "kr/claude-sonnet-4.5")


def local_llm(prompt: str) -> str:
    """
    Call local LLM endpoint using configuration from environment variables.

    Environment variables:
    - LLM_API_BASE: Base URL for the LLM API (default: http://localhost:20128/v1)
    - LLM_API_KEY: API key for authentication
    - LLM_MODEL: Model name to use (default: kr/claude-sonnet-4.5)
    """
    if not LLM_API_KEY:
        return "Error: LLM_API_KEY not set in environment variables"

    try:
        response = requests.post(
            f"{LLM_API_BASE}/chat/completions",
            headers={
                "Authorization": f"Bearer {LLM_API_KEY}",
                "Content-Type": "application/json"
            },
            json={
                "model": LLM_MODEL,
                "messages": [
                    {"role": "user", "content": prompt}
                ],
                "temperature": 0.7,
                "max_tokens": 500
            },
            timeout=30
        )
        response.raise_for_status()
        return response.json()["choices"][0]["message"]["content"]
    except requests.exceptions.RequestException as e:
        return f"Error calling LLM: {str(e)}"


def mock_llm(prompt: str) -> str:
    """Mock LLM for testing without real API calls."""
    return "This is a mock answer. To use real LLM, set LLM_API_KEY in .env file."


def main():
    print("=" * 60)
    print("RAG System Demo - Knowledge Base Agent")
    print("=" * 60)
    print()

    # Step 1: Create knowledge base
    print("📚 Step 1: Building Knowledge Base...")
    store = EmbeddingStore(collection_name="demo_kb")

    # Add sample documents about programming
    documents = [
        Document(
            id="doc1",
            content="Python is a high-level, interpreted programming language known for its simplicity and readability. It was created by Guido van Rossum and first released in 1991.",
            metadata={"topic": "python", "type": "intro"}
        ),
        Document(
            id="doc2",
            content="Python supports multiple programming paradigms including procedural, object-oriented, and functional programming. It has a large standard library and active community.",
            metadata={"topic": "python", "type": "features"}
        ),
        Document(
            id="doc3",
            content="Machine learning is a subset of artificial intelligence that enables systems to learn and improve from experience without being explicitly programmed. Popular Python libraries for ML include scikit-learn, TensorFlow, and PyTorch.",
            metadata={"topic": "machine_learning", "type": "intro"}
        ),
        Document(
            id="doc4",
            content="Vector databases store data as high-dimensional vectors and enable similarity search using techniques like cosine similarity. They are essential for building RAG (Retrieval-Augmented Generation) systems.",
            metadata={"topic": "vector_db", "type": "intro"}
        ),
        Document(
            id="doc5",
            content="RAG (Retrieval-Augmented Generation) combines information retrieval with language models. It first retrieves relevant documents from a knowledge base, then uses them as context for generating accurate answers.",
            metadata={"topic": "rag", "type": "intro"}
        ),
    ]

    store.add_documents(documents)
    print(f"✅ Added {store.get_collection_size()} documents to knowledge base")
    print()

    # Step 2: Choose LLM mode
    print("🤖 Step 2: Selecting LLM Mode...")
    print("Options:")
    print("  1. Mock LLM (no API calls, for testing)")
    print("  2. Real LLM (local endpoint at localhost:20128)")
    print()

    use_real_llm = input("Use Real LLM? (y/n, default=n): ").strip().lower() == 'y'

    if use_real_llm:
        print("✅ Using Real LLM (local endpoint)")
        llm_function = local_llm
    else:
        print("✅ Using Mock LLM")
        llm_function = mock_llm
    print()

    # Step 3: Create agent
    print("🚀 Step 3: Creating Knowledge Base Agent...")
    agent = KnowledgeBaseAgent(store=store, llm_fn=llm_function)
    print("✅ Agent ready!")
    print()

    # Step 4: Interactive Q&A
    print("=" * 60)
    print("💬 Interactive Q&A Session")
    print("=" * 60)
    print("Ask questions about the knowledge base (type 'quit' to exit)")
    print()

    # Sample questions
    sample_questions = [
        "What is Python?",
        "What is machine learning?",
        "How does RAG work?",
        "What are vector databases used for?",
    ]

    print("📝 Sample questions you can try:")
    for i, q in enumerate(sample_questions, 1):
        print(f"  {i}. {q}")
    print()

    # Q&A loop
    while True:
        question = input("❓ Your question: ").strip()

        if not question:
            continue

        if question.lower() in ['quit', 'exit', 'q']:
            print("\n👋 Goodbye!")
            break

        print(f"\n🔍 Searching knowledge base...")

        # Show retrieved context
        results = store.search(question, top_k=3)
        print(f"📄 Found {len(results)} relevant documents:")
        for i, result in enumerate(results, 1):
            print(f"  [{i}] (score: {result['score']:.3f}) {result['content'][:80]}...")
        print()

        # Get answer
        print("🤔 Generating answer...")
        answer = agent.answer(question, top_k=3)

        print("\n💡 Answer:")
        print("-" * 60)
        print(answer)
        print("-" * 60)
        print()


if __name__ == "__main__":
    main()
