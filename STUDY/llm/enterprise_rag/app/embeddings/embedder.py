from sentence_transformers import SentenceTransformer
# from app.config import EMBEDDING_MODEL_NAME
from enterprise_rag.app.config import EMBEDDING_MODEL_NAME


class LocalEmbedder:
    def __init__(self):
        self.model = SentenceTransformer(EMBEDDING_MODEL_NAME)

    def embed_text(self, text: str):
        return self.model.encode(text)

    def embed_batch(self, texts: list[str]):
        return self.model.encode(texts)
