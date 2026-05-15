import faiss
import pickle


class FAISSService:

    def __init__(self):

        self.index = faiss.read_index("embeddings/faiss_index.bin")

        with open("embeddings/chunks.pkl", "rb") as f:
            self.chunks = pickle.load(f)

    def search(self, query_embedding, k=3):

        distances, indices = self.index.search(
            query_embedding.reshape(1, -1),
            k
        )

        results = []

        for idx in indices[0]:
            results.append(self.chunks[idx])

        return results