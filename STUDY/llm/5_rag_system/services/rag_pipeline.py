# from services.embedding_service import EmbeddingService
# from services.faiss_service import FAISSService
# from services.llm_service import ask_llm


# class RAGPipeline:

#     def __init__(self):

#         self.embedder = EmbeddingService()

#         self.faiss = FAISSService()

#     def ask(self, question):

#         query_embedding = self.embedder.embed(question)

#         context_chunks = self.faiss.search(query_embedding)

#         context = "\n\n".join(context_chunks)

#         prompt = f"""
# Use the following context to answer the question.

# Context:
# {context}

# Question:
# {question}

# Answer:
# """

#         answer = ask_llm(prompt)

#         return answer
    


# from services.embedding_service import EmbeddingService
# from services.faiss_service import FAISSService
# from services.rerank_service import RerankService
# from services.llm_service import ask_llm


# class RAGPipeline:

#     def __init__(self):

#         self.embedder = EmbeddingService()
#         self.faiss = FAISSService()
#         self.reranker = RerankService()

#     def ask(self, question):

#         query_embedding = self.embedder.embed(question)

#         chunks = self.faiss.search(query_embedding, k=5)

#         ranked_chunks = self.reranker.rerank(question, chunks)

#         context = "\n\n".join(ranked_chunks[:3])

#         prompt = f"""
# Use the context below to answer.

# Context:
# {context}

# Question:
# {question}

# Answer:
# """

#         answer = ask_llm(prompt)

#         return answer




from services.embedding_service import EmbeddingService
from services.faiss_service import FAISSService
from services.rerank_service import RerankService
from services.bm25_service import BM25Service
from services.llm_service import ask_llm
from services.context_compressor import ContextCompressor


class RAGPipeline:

    def __init__(self, documents):

        self.embedder = EmbeddingService()
        self.faiss = FAISSService()
        self.reranker = RerankService()
        self.bm25 = BM25Service(documents)
        self.compressor = ContextCompressor()

    def ask(self, question):

        # query_embedding = self.embedder.embed(question)

        # vector_results = self.faiss.search(query_embedding, k=5)

        # keyword_results = self.bm25.search(question, k=5)

        # combined = list(set(vector_results + keyword_results))

        # ranked = self.reranker.rerank(question, combined)

        # context = "\n\n".join(ranked[:3])

        # Step 1: embed query
        query_embedding = self.embedder.embed(question)

        # Step 2: vector search
        vector_results = self.faiss.search(query_embedding, k=5)

        # Step 3: keyword search
        keyword_results = self.bm25.search(question, k=5)

        # Step 4: combine results
        combined = list(set(vector_results + keyword_results))

        # Step 5: rerank
        ranked = self.reranker.rerank(question, combined)

        # Step 6: compress context
        compressed = self.compressor.compress(question, ranked)

        # Step 7: build final context
        context = "\n".join(compressed[:5])


        prompt = f"""
Use the context below to answer.

Context:
{context}

Question:
{question}

Answer:
"""

        return ask_llm(prompt) 