import chromadb


class ChromaVectorStore:

    def __init__(self):

        self.client = chromadb.PersistentClient(
            path="data/chroma_db"
        )

        self.collection = self.client.get_or_create_collection(
            name="rag_collection"
        )

    def add_documents(
        self,
        embedded_chunks
    ):

        for chunk in embedded_chunks:

            self.collection.add(
                ids=[
                    str(chunk["chunk_id"])
                ],

                embeddings=[
                    chunk["embedding"]
                ],

                documents=[
                    chunk["content"]
                ],

                metadatas=[
                    {
                        "source": chunk["source"],
                        "chunk_id": chunk["chunk_id"]
                    }
                ]
            )

    def query(
        self,
        query_embedding,
        n_results=3
    ):

        results = self.collection.query(
            query_embeddings=[
                query_embedding
            ],

            n_results=n_results
        )

        return results