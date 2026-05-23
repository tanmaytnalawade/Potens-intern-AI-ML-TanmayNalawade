import gradio as gr
import requests


API_URL = "http://127.0.0.1:8000"


# -----------------------------------
# ASK QUESTION FUNCTION
# -----------------------------------

def ask_question(question):

    # Handle empty question
    if not question.strip():

        return (
            "✅ I'm ready to answer your question based on the provided context.\n\nPlease go ahead and ask your question.",
            "",
            ""
        )

    response = requests.post(
        f"{API_URL}/ask",
        json={
            "question": question
        }
    )

    data = response.json()

    answer = data["answer"]

    confidence = data.get("confidence")

    citations = data.get("citations", [])

    confidence_text = ""

    # Show confidence only if available
    if confidence is not None:

        confidence_text = (
            f"## Confidence Score\n\n"
            f"{int(confidence * 100)}%"
        )

    formatted_citations = ""

    # Show citations only if available
    if citations:

        for citation in citations:

            source_name = citation["source"].split("/")[-1]

            formatted_citations += f"""
### 📄 {source_name}

- **Chunk ID:** {citation['chunk_id']}

> {citation['snippet']}

---

"""

    return (
        answer,
        confidence_text,
        formatted_citations
    )


# -----------------------------------
# CONTRADICTION FUNCTION
# -----------------------------------

def contradict_documents(doc1, doc2):

    # Handle empty document paths
    if not doc1.strip() or not doc2.strip():

        return (
            "Please provide both document paths "
            "to check contradiction."
        )

    response = requests.post(
        f"{API_URL}/contradict",
        json={
            "doc1": doc1,
            "doc2": doc2
        }
    )

    data = response.json()

    return data["analysis"]


# -----------------------------------
# UI
# -----------------------------------

with gr.Blocks() as app:

    gr.Markdown(
        """
# RAG System with Citations and Contradiction Detection
"""
    )

    # -----------------------------------
    # ASK QUESTION TAB
    # -----------------------------------

    with gr.Tab("🔎 Ask Questions"):

        gr.Markdown(
            "### Ask a Question"
        )

        question_input = gr.Textbox(
            placeholder=(
                "Examples:\n"
                "• What is Retrieval-Augmented Generation?\n"
                "• What is Transformer architecture?\n"
                "• रिट्रीवल ऑगमेंटेड जनरेशन क्या है?"
            ),
            lines=4
        )

        ask_button = gr.Button(
            "Ask Question"
        )

        answer_output = gr.Markdown(
            label="Answer"
        )

        confidence_output = gr.Markdown()

        citations_output = gr.Markdown()

        ask_button.click(
            fn=ask_question,
            inputs=question_input,
            outputs=[
                answer_output,
                confidence_output,
                citations_output
            ]
        )

    # -----------------------------------
    # CONTRADICTION TAB
    # -----------------------------------

    with gr.Tab("⚖️ Contradiction Detection"):

        gr.Markdown(
            "### Compare Two Documents"
        )

        doc1_input = gr.Textbox(
            label="Document 1 Path",
            placeholder="docs/rag_paper.pdf"
        )

        doc2_input = gr.Textbox(
            label="Document 2 Path",
            placeholder="docs/transformer_paper.pdf"
        )

        contradict_button = gr.Button(
            "Check Contradiction"
        )

        contradiction_output = gr.Markdown()

        contradict_button.click(
            fn=contradict_documents,
            inputs=[
                doc1_input,
                doc2_input
            ],
            outputs=contradiction_output
        )


app.launch(
    inbrowser=True
)