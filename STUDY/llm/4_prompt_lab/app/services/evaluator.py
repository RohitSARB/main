from nltk.translate.bleu_score import sentence_bleu, SmoothingFunction
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np


# -----------------------------
# BLEU SCORE
# -----------------------------
def calculate_bleu(reference: str, candidate: str) -> float:
    reference_tokens = reference.split()
    candidate_tokens = candidate.split()

    smoothie = SmoothingFunction().method1
    score = sentence_bleu(
        [reference_tokens],
        candidate_tokens,
        smoothing_function=smoothie
    )

    return round(score, 4)


# -----------------------------
# COSINE SIMILARITY
# -----------------------------
def calculate_similarity(reference: str, candidate: str) -> float:
    vectorizer = TfidfVectorizer()
    vectors = vectorizer.fit_transform([reference, candidate])

    sim = cosine_similarity(vectors[0:1], vectors[1:2])[0][0]

    return round(float(sim), 4)
