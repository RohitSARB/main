class ContextCompressor:
    def compress(self, query, documents):
        compressed = []

        for doc in documents:
            sentences = doc.split(".")
            for s in sentences:
                if any(word in s.lower() for word in query.lower().split()):
                    compressed.append(s.strip())

        return compressed