# import faiss
# import numpy as np

# dimensions = 4

# vectors = np.array([
#     [1.0, 0.0, 0.0, 0.0],
#     [0.9, 0.1, 0.0, 0.0],
#     [-1.0, 0.0, 0.0, 0.0],
#     [0.0, 1.0, 0.0, 0.0]
# ]).astype("float32")

# index = faiss.IndexFlatL2(dimensions)

# index.add(vectors)

# print("vectors: ", index)
# print("total vectors: ", index.ntotal)

# query = np.array([[0.8, 0.2, 0.0, 0.0]]).astype("float32")

# # k=2 # top nearest
# # distances, indices = index.search(query, k)

# k=3
# distances, indices = index.search(query, k)
# for i in indices[0]:
#     print(vectors[i])

# print("Distances: ",distances)
# print("Indices: ",indices)




import faiss
import numpy as np

dimension = 4

vectors = np.array([
    [1,0,0,0],
    [0.9,0.1,0,0],
    [-1,0,0,0],
    [0,1,0,0]
]).astype("float32")

# normalize vectors
faiss.normalize_L2(vectors)

# cosine similarity index
index = faiss.IndexFlatIP(dimension)

index.add(vectors)

query = np.array([[0.8,0.2,0,0]]).astype("float32")
faiss.normalize_L2(query)

k = 2

distances, indices = index.search(query, k)

print("Indices:", indices)
print("Similarity:", distances)