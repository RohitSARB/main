import numpy as np
from typing import List, Dict
from services.embedding_service import get_embedding


class SimpleVectorStore:

    def __init__(self):
        self.vectors = []
        self.texts = []
        self.metadata = []

    def add_documents(self, chunks: List[str], meta: Dict = None):
        """
            Embed and store chunks
        """
        for idx, chunk in enumerate(chunks):
            embedding = np.array(get_embedding(chunk))
            self.vectors.append(embedding)
            self.texts.append(chunk)
            self.metadata.append({
                "chunk_index": idx,
                **(meta or {})
            })
    
    def similarity_search(self, query: str, top_k: int = 3):
        """
        Return top_k most similar chunks
        """
        query_vector = np.array(get_embedding(query))

        similarities = []

        for idx, vector in enumerate(self.vectors):
            sim = self.cosine_similarity(query_vector, vector)
            similarities.append((sim,idx))

        similarities.sort(reverse=True, key=lambda x: x[0])

        top_results = []

        for score, idx in similarities[:top_k]:
            top_results.append({
                "score":float(score),
                "text":self.texts[idx],
                "metadata": self.metadata[idx]
            })
        
        return top_results
    
    @staticmethod
    def cosine_similarity(vec1,vec2):
        return np.dot(vec1,vec2) / (
            np.linalg.norm(vec1)*np.linalg.norm(vec2)
        )
    


if __name__ == "__main__":
    from services.chunker import recursive_chunk_text

    document = """
    Refunds are allowed within 30 days of purchase.
    Shipping takes 3-5 business days.
    Returns must be unused and in original packaging.
    """

    chunks = recursive_chunk_text(document, chunk_size=50, overlap=10)

    store = SimpleVectorStore()
    store.add_documents(chunks)

    results = store.similarity_search(
        "What is the refund window?",
        top_k=2
    )

    print("\nTop Results:\n")
    for r in results:
        print("Score:", r["score"])
        print("Text:", r["text"])
        print("-" * 50)