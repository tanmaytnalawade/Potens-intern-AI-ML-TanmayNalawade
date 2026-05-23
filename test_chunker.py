from core.chunker import DocumentChunker


chunker = DocumentChunker()

chunks = chunker.process_pdf(
    "docs/rag_paper.pdf"
)

print(
    f"Total Chunks: {len(chunks)}"
)

print("\nFIRST CHUNK:\n")

print(chunks[0])