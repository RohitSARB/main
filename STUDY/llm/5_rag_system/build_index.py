import faiss
import pickle

from sentence_transformers import SentenceTransformer

from services.chunk_service import chunk_text


model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")


with open("data/documents.txt", "r", encoding="utf-8") as f:
    text = f.read()


chunks = chunk_text(text)

print("Total chunks:", len(chunks))


embeddings = model.encode(chunks)


dimension = embeddings.shape[1]

index = faiss.IndexFlatL2(dimension)

index.add(embeddings)


faiss.write_index(index, "embeddings/faiss_index.bin")


with open("embeddings/chunks.pkl", "wb") as f:
    pickle.dump(chunks, f)

print("FAISS index built successfully")