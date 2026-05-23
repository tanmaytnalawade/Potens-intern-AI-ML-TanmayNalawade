from core.retriever import Retriever


retriever = Retriever()

results = retriever.retrieve(
    "What is Retrieval-Augmented Generation?"
)

print("\nRETRIEVED RESULTS:\n")

for index, result in enumerate(results):

    print(f"\nRESULT {index + 1}\n")

    print(result["metadata"])

    print("\nCONTENT:\n")

    print(result["content"][:500])