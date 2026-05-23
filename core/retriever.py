from core.embedder import EmbeddingGenerator
from store.chroma_store import ChromaVectorStore


class Retriever:

    def __init__(self):

        self.embedder = EmbeddingGenerator()

        self.vector_store = ChromaVectorStore()

    def retrieve(
        self,
        query,
        n_results=3
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

            retrieved_chunks.append({
                "content": document,
                "metadata": metadata
            })

        return retrieved_chunks