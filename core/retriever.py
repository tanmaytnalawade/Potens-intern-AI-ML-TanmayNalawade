from core.embedder import EmbeddingGenerator
from store.chroma_store import ChromaVectorStore


class Retriever:

    def __init__(self):

        self.embedder = EmbeddingGenerator()

        self.vector_store = ChromaVectorStore()

    def retrieve(
        self,
        query,
        n_results=5
    ):

        query_embedding = self.embedder.generate_embedding(
            query
        )

        results = self.vector_store.query(
            query_embedding,
            n_results
        )

        retrieved_chunks = []

        documents = results["documents"][0]

        metadatas = results["metadatas"][0]

        for document, metadata in zip(
            documents,
            metadatas
        ):

            # Skip title-heavy first chunk
            if metadata["chunk_id"] == 0:
                continue

            # Skip very small chunks
            if len(document.strip()) < 100:
                continue

            retrieved_chunks.append({
                "content": document,
                "metadata": metadata
            })

        return retrieved_chunks