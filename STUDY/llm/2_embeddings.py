from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

model = SentenceTransformer("all-MiniLM-L6-v2")

sentences = [
    "FastAPI is great for backend development",
    "MongoDB works well with Python",
    "The cat is sleeping on the sofa"
]

embeddings = model.encode(sentences)
print(embeddings)
similarity = cosine_similarity([embeddings[0]],embeddings[1:])
print(similarity)