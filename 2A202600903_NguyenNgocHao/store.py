from __future__ import annotations

from typing import Any, Callable

from .chunking import _dot
from .embeddings import _mock_embed
from .models import Document


class EmbeddingStore:
    """
    A vector store for text chunks.

    Tries to use ChromaDB if available; falls back to an in-memory store.
    The embedding_fn parameter allows injection of mock embeddings for tests.
    """

    def __init__(
        self,
        collection_name: str = "documents",
        embedding_fn: Callable[[str], list[float]] | None = None,
    ) -> None:
        self._embedding_fn = embedding_fn or _mock_embed
        self._collection_name = collection_name
        self._use_chroma = False
        self._store: list[dict[str, Any]] = []
        self._collection = None
        self._next_index = 0

        try:
            import chromadb  # noqa: F401

            # TODO: initialize chromadb client + collection
            self._use_chroma = True
        except Exception:
            self._use_chroma = False
            self._collection = None

    def _make_record(self, doc: Document) -> dict[str, Any]:
        """Build a normalized stored record for one document."""
        embedding = self._embedding_fn(doc.content)
        record = {
            "id": f"doc_{self._next_index}",
            "text": doc.content,
            "embedding": embedding,
            "metadata": {**doc.metadata, "doc_id": doc.id}
        }
        self._next_index += 1
        return record

    def _search_records(self, query: str, records: list[dict[str, Any]], top_k: int) -> list[dict[str, Any]]:
        """Run in-memory similarity search over provided records."""
        if not records:
            return []

        # Embed the query
        query_embedding = self._embedding_fn(query)

        # Calculate similarity for each record
        scored_records = []
        for record in records:
            similarity = _dot(query_embedding, record["embedding"])
            scored_records.append((similarity, record))

        # Sort by similarity (descending) and return top_k
        scored_records.sort(key=lambda x: x[0], reverse=True)

        # Format results to match test expectations
        results = []
        for score, record in scored_records[:top_k]:
            results.append({
                "content": record["text"],
                "score": score,
                "metadata": record["metadata"]
            })
        return results

    def add_documents(self, docs: list[Document]) -> None:
        """
        Embed each document's content and store it.

        For ChromaDB: use collection.add(ids=[...], documents=[...], embeddings=[...])
        For in-memory: append dicts to self._store
        """
        if not docs:
            return

        if self._use_chroma and self._collection is not None:
            # ChromaDB mode
            ids = []
            documents = []
            embeddings = []
            metadatas = []

            for doc in docs:
                record = self._make_record(doc)
                ids.append(record["id"])
                documents.append(record["text"])
                embeddings.append(record["embedding"])
                metadatas.append(record["metadata"])

            self._collection.add(
                ids=ids,
                documents=documents,
                embeddings=embeddings,
                metadatas=metadatas
            )
        else:
            # In-memory mode
            for doc in docs:
                record = self._make_record(doc)
                self._store.append(record)

    def search(self, query: str, top_k: int = 5) -> list[dict[str, Any]]:
        """
        Find the top_k most similar documents to query.

        For in-memory: compute dot product of query embedding vs all stored embeddings.
        """
        if self._use_chroma and self._collection is not None:
            # ChromaDB mode
            query_embedding = self._embedding_fn(query)
            results = self._collection.query(
                query_embeddings=[query_embedding],
                n_results=top_k
            )

            # Convert ChromaDB results to our format
            found = []
            if results["ids"] and results["ids"][0]:
                for i, doc_id in enumerate(results["ids"][0]):
                    found.append({
                        "content": results["documents"][0][i] if results["documents"] else "",
                        "score": 1.0 - results["distances"][0][i] if results.get("distances") else 0.0,
                        "metadata": results["metadatas"][0][i] if results["metadatas"] else {}
                    })
            return found
        else:
            # In-memory mode
            return self._search_records(query, self._store, top_k)

    def get_collection_size(self) -> int:
        """Return the total number of stored chunks."""
        if self._use_chroma and self._collection is not None:
            # ChromaDB mode
            return self._collection.count()
        else:
            # In-memory mode
            return len(self._store)

    def search_with_filter(self, query: str, top_k: int = 3, metadata_filter: dict = None) -> list[dict]:
        """
        Search with optional metadata pre-filtering.

        First filter stored chunks by metadata_filter, then run similarity search.
        """
        if self._use_chroma and self._collection is not None:
            # ChromaDB mode with where filter
            query_embedding = self._embedding_fn(query)
            results = self._collection.query(
                query_embeddings=[query_embedding],
                n_results=top_k,
                where=metadata_filter if metadata_filter else None
            )

            # Convert ChromaDB results to our format
            found = []
            if results["ids"] and results["ids"][0]:
                for i, doc_id in enumerate(results["ids"][0]):
                    found.append({
                        "content": results["documents"][0][i] if results["documents"] else "",
                        "score": 1.0 - results["distances"][0][i] if results.get("distances") else 0.0,
                        "metadata": results["metadatas"][0][i] if results["metadatas"] else {}
                    })
            return found
        else:
            # In-memory mode: filter first, then search
            if metadata_filter is None:
                filtered_records = self._store
            else:
                filtered_records = []
                for record in self._store:
                    # Check if all filter key-value pairs match
                    matches = all(
                        record["metadata"].get(key) == value
                        for key, value in metadata_filter.items()
                    )
                    if matches:
                        filtered_records.append(record)

            return self._search_records(query, filtered_records, top_k)

    def delete_document(self, doc_id: str) -> bool:
        """
        Remove all chunks belonging to a document.

        Returns True if any chunks were removed, False otherwise.
        """
        if self._use_chroma and self._collection is not None:
            # ChromaDB mode: delete by metadata filter
            try:
                self._collection.delete(where={"doc_id": doc_id})
                return True
            except Exception:
                return False
        else:
            # In-memory mode: filter out matching records
            original_size = len(self._store)
            self._store = [
                record for record in self._store
                if record["metadata"].get("doc_id") != doc_id
            ]
            return len(self._store) < original_size
