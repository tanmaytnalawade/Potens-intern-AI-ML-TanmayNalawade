from core.retriever import Retriever
from core.llm import LLMService


retriever = Retriever()

retrieved_chunks = retriever.retrieve(
    "What is Retrieval-Augmented Generation?"
)

llm = LLMService()

answer = llm.generate_answer(
    question="Who won FIFA World Cup 2022?",
    retrieved_chunks=retrieved_chunks
)

print("\nANSWER:\n")

print(answer)