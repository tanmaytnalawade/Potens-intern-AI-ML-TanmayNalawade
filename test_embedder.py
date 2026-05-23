from core.chunker import DocumentChunker
from core.embedder import EmbeddingGenerator


chunker = DocumentChunker()

chunks = chunker.process_pdf(
    "docs/rag_paper.pdf"
)

embedder = EmbeddingGenerator()

embedded_chunks = embedder.embed_chunks(
    chunks[:1]
)

print("\nEMBEDDED DOCUMENT:\n")

print(
    embedded_chunks[0].keys()
)

print("\nEmbedding Length:\n")

print(
    len(
        embedded_chunks[0]["embedding"]
    )
)