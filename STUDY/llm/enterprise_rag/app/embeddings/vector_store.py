import faiss
import numpy as np
import os
from enterprise_rag.app.config import FAISS_INDEX_PATH


class VectorStore:
    def __init__(self, dimension: int):
        self.dimension = dimension
        self.index = faiss.IndexFlatL2(dimension)

    def add_embeddings(self, embeddings: list):
        vectors = np.array(embeddings).astype("float32")
        self.index.add(vectors)

    def search(self, query_vector, top_k=5):
        query_vector = np.array([query_vector]).astype("float32")
        distances, indices = self.index.search(query_vector, top_k)
        return distances, indices

    def save(self):
        faiss.write_index(self.index, FAISS_INDEX_PATH)

    def load(self):
        if os.path.exists(FAISS_INDEX_PATH):
            self.index = faiss.read_index(FAISS_INDEX_PATH)