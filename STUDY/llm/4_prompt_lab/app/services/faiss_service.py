import faiss
import numpy as np
from app.services.embedding_service import get_embedding


class FAISSService:

    def __init__(self, dimension=384):

        self.dimension = dimension

        # cosine similarity index
        self.index = faiss.IndexFlatIP(dimension)

        # store text chunks
        self.text_store = []

    def add_texts(self, texts):

        embeddings = []

        for text in texts:
            emb = get_embedding(text)
            embeddings.append(emb)
            self.text_store.append(text)

        embeddings = np.array(embeddings).astype("float32")

        # normalize for cosine similarity
        faiss.normalize_L2(embeddings)

        self.index.add(embeddings)

    def search(self, query, k=3):

        query_embedding = np.array(
            [get_embedding(query)]
        ).astype("float32")

        faiss.normalize_L2(query_embedding)

        distances, indices = self.index.search(query_embedding, k)

        results = []

        for idx in indices[0]:
            results.append(self.text_store[idx])

        return results
    


if '__name__' == 'main':

    docs = [
        "Refunds are allowed within 30 days.",
        "Shipping takes 5 to 7 business days.",
        "You can reset your password from settings.",
        "Contact support for billing questions."
    ]

    faiss_service = FAISSService()

    faiss_service.add_texts(docs)

    query = "How do I get my money back?"

    results = faiss_service.search(query)

    print("\nTop results:\n")

    for r in results:
        print("-", r)