from services.rag_service import RAGService


rag = RAGService()

document = """
Refunds are allowed within 30 days of purchase.
Shipping takes 3-5 business days.
Returns must be unused and in original packaging.
"""

rag.ingest_document(document)

question = "How many days do I have to request a refund?"

answer = rag.answer_question(question)

print("\nAnswer:\n")
print(answer)