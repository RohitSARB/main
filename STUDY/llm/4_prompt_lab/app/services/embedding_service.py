# import os
# import requests
# from typing import List
# from dotenv import load_dotenv

# load_dotenv()

# # HF_API_TOKEN = os.getenv("HF_API_TOKEN")
# HF_API_TOKEN = 'csk-ne2dje933kdehkvtdcdveve6vrmvmx48jwed6h4wt5fvtxmd'
# MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"

# API_URL = f"https://router.huggingface.co/hf-inference/models/{MODEL_NAME}"

# headers = {
#     "Authorization": f"Bearer {HF_API_TOKEN}",
#     "Content-Type": "application/json"
# }


# # def get_embedding(text: str) -> List[float]:
# #     response = requests.post(
# #         API_URL,
# #         headers=headers,
# #         json={"inputs": text}
# #     )

# #     if response.status_code != 200:
# #         raise Exception(
# #             f"Embedding API Error: {response.status_code} - {response.text}"
# #         )

# #     embedding = response.json()

# #     # Some models return nested list
# #     if isinstance(embedding[0], list):
# #         embedding = embedding[0]

# #     return embedding

# def get_embedding(text: str):
#     url = "https://router.huggingface.co/v1/embeddings"

#     headers = {
#         "Authorization": f"Bearer {HF_API_TOKEN}",
#         "Content-Type": "application/json"
#     }

#     payload = {
#         "model": "sentence-transformers/all-MiniLM-L6-v2",
#         "input": text
#     }

#     response = requests.post(url, headers=headers, json=payload)

#     if response.status_code != 200:
#         raise Exception(
#             f"Embedding API Error: {response.status_code} - {response.text}"
#         )

#     data = response.json()
#     return data["data"][0]["embedding"]


# # ---- Quick test ----
# if __name__ == "__main__":
#     text = "Refunds are allowed within 30 days."
#     # print("HF_API_TOKEN:", HF_API_TOKEN)
#     vector = get_embedding(text)
#     print("Vector length:", len(vector))
#     print("First 5 values:", vector[:5])





from sentence_transformers import SentenceTransformer
from typing import List
import numpy as np

# Load model once (important)
model = SentenceTransformer("all-MiniLM-L6-v2")


def get_embedding(text: str) -> List[float]:
    """
    Generate embedding for given text
    """
    embedding = model.encode(text, convert_to_numpy=True)
    return embedding.tolist()


# ---- Quick test ----
if __name__ == "__main__":
    text = "Refunds are allowed within 30 days."
    vector = get_embedding(text)
    print("Vector length:", len(vector))
    print("First 5 values:", vector[:5])
    print("First 5 values:", vector)