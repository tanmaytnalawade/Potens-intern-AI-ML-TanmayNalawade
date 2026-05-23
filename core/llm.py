from groq import Groq
from dotenv import load_dotenv
import os


load_dotenv()


class LLMService:

    def __init__(self):

        self.client = Groq(
            api_key=os.getenv(
                "GROQ_API_KEY"
            )
        )

    def generate_answer(
        self,
        question,
        retrieved_chunks
    ):

        context = "\n\n".join([
            chunk["content"]
            for chunk in retrieved_chunks
        ])

        prompt = f"""
You are a helpful AI assistant.

Answer the question ONLY using the provided context.

If the answer is not available in the context, say:
"I could not find the answer in the provided documents."

Context:
{context}

Question:
{question}

Answer:
"""

        response = self.client.chat.completions.create(

            model="llama-3.1-8b-instant",

            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ],

            temperature=0
        )

        answer = response.choices[0].message.content

        return answer