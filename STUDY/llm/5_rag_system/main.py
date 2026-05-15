from services.rag_pipeline import RAGPipeline


rag = RAGPipeline()

# while True:

question = input("\nAsk a question: ")
answer = rag.ask(question)
print("\nAnswer:\n", answer)