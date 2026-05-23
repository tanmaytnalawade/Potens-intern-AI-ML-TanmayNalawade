from fastapi import APIRouter
from pydantic import BaseModel

from core.retriever import Retriever
from core.llm import LLMService
from services.citation_service import CitationService


router = APIRouter()


retriever = Retriever()

llm = LLMService()

citation_service = CitationService()


class QuestionRequest(BaseModel):

    question: str


@router.post("/ask")
def ask_question(request: QuestionRequest):

    retrieved_chunks = retriever.retrieve(
        request.question
    )

    answer = llm.generate_answer(
        question=request.question,
        retrieved_chunks=retrieved_chunks
    )

    citations = citation_service.generate_citations(
        retrieved_chunks
    )

    return {

        "question": request.question,

        "answer": answer,

        "citations": citations
    }