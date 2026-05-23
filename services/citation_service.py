class CitationService:

    def generate_citations(
        self,
        retrieved_chunks
    ):

        citations = []

        for chunk in retrieved_chunks:

            citation = {

                "source": chunk["metadata"]["source"],

                "chunk_id": chunk["metadata"]["chunk_id"],

                "snippet": chunk["content"][:350]

            }

            citations.append(
                citation
            )

        return citations