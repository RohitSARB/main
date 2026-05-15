from services.chunker import recursive_chunk_text
from services.vector_store import SimpleVectorStore
from services.llm_service import ask_llm


class RAGService:

    def __init__(self):
        self.vector_store = SimpleVectorStore()

    def ingest_document(self, document: str):
        """
        Chunk and store document in vector DB
        """
        chunks = recursive_chunk_text(document, chunk_size=200, overlap=40)
        self.vector_store.add_documents(chunks)

    def answer_question(self, question: str):
        """
        Retrieve relevant chunks and ask LLM
        """

        results = self.vector_store.similarity_search(
            question,
            top_k=3
        )

        context = "\n\n".join([r["text"] for r in results])

        prompt = f"""
You are a helpful assistant.

Answer the question ONLY using the context below.

Context:
{context}

Question:
{question}

Answer:
"""

        response = ask_llm(prompt)

        return response