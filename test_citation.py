from core.retriever import Retriever
from services.citation_service import CitationService


retriever = Retriever()

retrieved_chunks = retriever.retrieve(
    "What is Retrieval-Augmented Generation?"
)

citation_service = CitationService()

citations = citation_service.generate_citations(
    retrieved_chunks
)

print("\nCITATIONS:\n")

for citation in citations:

    print(citation)

    print("\n-------------------\n")