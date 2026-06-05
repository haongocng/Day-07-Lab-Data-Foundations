import os
import sys
from pathlib import Path

# Add project root to PYTHONPATH
project_root = Path(__file__).resolve().parent
sys.path.append(str(project_root))

from src.agent import KnowledgeBaseAgent
from src.embeddings import _mock_embed
from src.models import Document
from src.store import EmbeddingStore

def load_documents_from_dir(data_dir: str) -> list[Document]:
    """Load all .md and .txt files from the given directory (recursively)."""
    allowed = {'.md', '.txt'}
    docs = []
    for path in Path(data_dir).rglob('*'):
        if path.suffix.lower() in allowed and path.is_file():
            docs.append(Document(
                id=path.stem,
                content=path.read_text(encoding='utf-8'),
                metadata={'source': str(path), 'extension': path.suffix.lower()},
            ))
    return docs

def demo_law_data(query: str = "Trích xuất đoạn luật vị trí đường bộ") -> None:
    data_dir = os.path.join('data', 'Data_Law_Transportation')
    docs = load_documents_from_dir(data_dir)
    print(f"Loaded {len(docs)} law documents.")
    embedder = _mock_embed  # using mock embedder for quick demo
    store = EmbeddingStore(collection_name='law_demo', embedding_fn=embedder)
    store.add_documents(docs)
    agent = KnowledgeBaseAgent(store=store, llm_fn=lambda q: f"[MOCK] Answer to: {q}")
    print("Query:", query)
    print("Agent answer:\n", agent.answer(query, top_k=3))

if __name__ == "__main__":
    demo_law_data()
