from fastapi import APIRouter
from pydantic import BaseModel

from core.retriever import Retriever
from core.llm import LLMService
from core.translator import TranslatorService
from services.citation_service import CitationService


router = APIRouter()


retriever = Retriever()

llm = LLMService()

translator = TranslatorService()

citation_service = CitationService()


class QuestionRequest(BaseModel):

    question: str


@router.post("/ask")
def ask_question(request: QuestionRequest):

    if not request.question.strip():

        return {

            "question": "",

            "language": "en",

            "answer": (
                "I'm ready to answer your question "
                "based on the provided context. "
                "Please go ahead and ask your question."
            ),

            "confidence": None,

            "citations": []
        }

    detected_language = translator.detect_language(
        request.question
    )

    translated_question = request.question

    if detected_language != "en":

        translated_question = translator.translate_to_english(
            request.question
        )

    retrieved_chunks = retriever.retrieve(
        translated_question
    )

    answer = llm.generate_answer(
        question=translated_question,
        retrieved_chunks=retrieved_chunks
    )

    if detected_language != "en":

        answer = translator.translate_from_english(
            answer,
            detected_language
        )

    citations = citation_service.generate_citations(
        retrieved_chunks
    )

    # Simple confidence heuristic
    confidence = round(
        0.95 - (len(citations) * 0.01),
        2
    )

    if (
        "I could not find the answer"
        in answer
    ):

        confidence = None

        citations = []

    return {

        "question": request.question,

        "language": detected_language,

        "answer": answer,

        "confidence": confidence,

        "citations": citations
    }