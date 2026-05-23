from fastapi import APIRouter
from pydantic import BaseModel

from core.chunker import DocumentChunker
from core.llm import LLMService


router = APIRouter()


chunker = DocumentChunker()

llm = LLMService()


class ContradictionRequest(BaseModel):

    doc1: str

    doc2: str


@router.post("/contradict")
def detect_contradiction(
    request: ContradictionRequest
):

    doc1_chunks = chunker.process_pdf(
        request.doc1
    )

    doc2_chunks = chunker.process_pdf(
        request.doc2
    )

    doc1_text = "\n".join([
        chunk["content"]
        for chunk in doc1_chunks[:3]
    ])

    doc2_text = "\n".join([
        chunk["content"]
        for chunk in doc2_chunks[:3]
    ])

    prompt = f"""
You are an AI system that detects contradictions between two documents.

Document 1:
{doc1_text}

Document 2:
{doc2_text}

Analyze whether the documents contradict each other.

Return:
- Contradiction: YES or NO
- Reasoning
"""

    response = llm.client.chat.completions.create(

        model="llama-3.1-8b-instant",

        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],

        temperature=0
    )

    analysis = response.choices[0].message.content

    return {

        "doc1": request.doc1,

        "doc2": request.doc2,

        "analysis": analysis
    }