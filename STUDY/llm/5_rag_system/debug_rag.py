from services.rag_debugger import RAGDebugger


documents = open("data/documents.txt").read().split("\n\n")

rag = RAGDebugger(documents)

question = "What is FAISS?"

rag.ask(question)