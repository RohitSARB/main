from app.retrieval.retriever import Retriever
from app.llm.llm_client import LLMClient


class RAGPipeline:
    def __init__(self):
        self.retriever = Retriever()
        self.llm = LLMClient()

    def run(self, question: str) -> str:
        # 1️ Retrieve
        context = self.retriever.retrieve(question)

        # 2️ Generate Answer
        answer = self.llm.generate_answer(question, context)

        return answer
