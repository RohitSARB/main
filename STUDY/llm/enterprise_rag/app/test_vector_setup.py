from enterprise_rag.app.embeddings.embedder import LocalEmbedder
from enterprise_rag.app.embeddings.vector_store import VectorStore

texts = [
    "OAuth is an authorization framework.",
    "JWT is used for authentication.",
    "Microservices use API gateways."
]

embedder = LocalEmbedder()
embeddings = embedder.embed_batch(texts)

dimension = len(embeddings[0])
vector_store = VectorStore(dimension)
vector_store.add_embeddings(embeddings)

query = embedder.embed_text("What is OAuth?")
distances, indices = vector_store.search(query, top_k=2)

print("Top matches:", indices)
