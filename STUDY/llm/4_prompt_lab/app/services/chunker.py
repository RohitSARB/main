from typing import List


def recursive_chunk_text(
    text: str,
    chunk_size: int = 700,
    overlap: int = 130
):
    words = text.split()
    chunks = []

    start = 0
    text_length = len(words)

    while start < text_length:
        end = min(start + chunk_size, text_length)

        chunk = words[start:end]
        chunks.append(" ".join(chunk))

        # If we've reached the end, stop
        if end == text_length:
            break

        start = end - overlap

    return chunks


# ---- Quick test ----
if __name__ == "__main__":
    sample_text = "This is a test document. " * 200
    print(sample_text)
    result = recursive_chunk_text(sample_text)

    print("Total chunks:", len(result))
    print("First chunk length:", len(result[0].split()))