import fitz


class DocumentChunker:

    def __init__(
        self,
        chunk_size=500,
        chunk_overlap=100
    ):

        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap

    def extract_text_from_pdf(self, pdf_path):

        document = fitz.open(pdf_path)

        text = ""

        for page in document:

            text += page.get_text()

        return text

    def chunk_text(
        self,
        text,
        source
    ):

        chunks = []

        start = 0

        chunk_id = 0

        while start < len(text):

            end = start + self.chunk_size

            chunk = text[start:end]

            chunks.append({
                "chunk_id": chunk_id,
                "source": source,
                "content": chunk
            })

            start += (
                self.chunk_size -
                self.chunk_overlap
            )

            chunk_id += 1

        return chunks

    def process_pdf(
        self,
        pdf_path
    ):

        text = self.extract_text_from_pdf(
            pdf_path
        )

        chunks = self.chunk_text(
            text,
            pdf_path
        )

        return chunks