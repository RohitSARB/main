from services.rag_pipeline import RAGPipeline

documents = open("data/documents.txt").read().split("\n\n")

rag = RAGPipeline(documents)


def rag_search(query):
    return rag.ask(query)