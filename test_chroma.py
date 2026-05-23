from core.chunker import DocumentChunker
from core.embedder import EmbeddingGenerator
from store.chroma_store import ChromaVectorStore


chunker = DocumentChunker()

chunks = chunker.process_pdf(
    "docs/rag_paper.pdf"
)

embedder = EmbeddingGenerator()

embedded_chunks = embedder.embed_chunks(
    chunks[:5]
)

vector_store = ChromaVectorStore()

vector_store.add_documents(
    embedded_chunks
)

print(
    "Documents stored successfully!"
)