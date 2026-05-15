from app.services_2.vector_store import VectorStore
from app.services.embedding_service import get_embedding

store = VectorStore()

docs = [
    "Python is a programming language",
    "Transformers power modern AI models",
    "Vector databases are used in RAG",
]

embeddings = [get_embedding(d) for d in docs]

store.add_embeddings(embeddings, docs)

query = "What are vector databases?"

query_vector = get_embedding(query)

results = store.search(query_vector)

print(results)