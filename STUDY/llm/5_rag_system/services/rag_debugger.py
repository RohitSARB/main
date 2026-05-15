from services.embedding_service import EmbeddingService
from services.faiss_service import FAISSService
from services.rerank_service import RerankService
from services.bm25_service import BM25Service
from services.llm_service import ask_llm


class RAGDebugger:

    def __init__(self, documents):

        self.embedder = EmbeddingService()
        self.faiss = FAISSService()
        self.reranker = RerankService()
        self.bm25 = BM25Service(documents)

    def ask(self, question):

        print("\n==============================")
        print("QUESTION:", question)
        print("==============================\n")

        query_embedding = self.embedder.embed(question)

        # Vector retrieval
        vector_results = self.faiss.search(query_embedding, k=5)

        print("VECTOR SEARCH RESULTS:")
        for r in vector_results:
            print("-", r[:120])
        print()

        # Keyword retrieval
        keyword_results = self.bm25.search(question, k=5)

        print("BM25 RESULTS:")
        for r in keyword_results:
            print("-", r[:120])
        print()

        # Combine
        combined = list(set(vector_results + keyword_results))

        print("COMBINED RESULTS:", len(combined))
        print()

        # Rerank
        ranked = self.reranker.rerank(question, combined)

        print("RERANKED RESULTS:")
        for r in ranked[:3]:
            print("-", r[:120])
        print()

        # Final context
        context = "\n\n".join(ranked[:3])

        print("FINAL CONTEXT:")
        print(context)
        print()

        prompt = f"""
Use the context below to answer.

Context:
{context}

Question:
{question}

Answer:
"""

        answer = ask_llm(prompt)

        print("FINAL ANSWER:")
        print(answer)
        print()

        return answer