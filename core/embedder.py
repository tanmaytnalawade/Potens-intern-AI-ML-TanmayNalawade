from sentence_transformers import SentenceTransformer


class EmbeddingGenerator:

    def __init__(self):

        self.model = SentenceTransformer(
            "all-MiniLM-L6-v2"
        )

    def generate_embedding(
        self,
        text
    ):

        embedding = self.model.encode(
            text
        )

        return embedding.tolist()

    def embed_chunks(
        self,
        chunks
    ):

        embedded_chunks = []

        for chunk in chunks:

            embedding = self.generate_embedding(
                chunk["content"]
            )

            chunk["embedding"] = embedding

            embedded_chunks.append(
                chunk
            )

        return embedded_chunks