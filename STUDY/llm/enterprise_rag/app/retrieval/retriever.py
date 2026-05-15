from app.vectorstore.faiss_store import VectorStore
from app.embeddings.embedder import Embedder


class Retriever:
    def __init__(self):
        self.embedder = Embedder()
        self.vectorstore = VectorStore()

    def retrieve(self, query: str, top_k: int = 3):
        query_vector = self.embedder.embed_query(query)
        results = self.vectorstore.search(query_vector, top_k)

        contexts = [res["text"] for res in results]
        return "\n\n".join(contexts)
