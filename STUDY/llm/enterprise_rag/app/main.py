from fastapi import FastAPI
from app.schemas.query_schema import QueryRequest
from app.services.rag_pipeline import RAGPipeline

app = FastAPI(title="Enterprise Hybrid RAG")

rag = RAGPipeline()


@app.post("/ask")
def ask_question(request: QueryRequest):
    answer = rag.run(request.question)
    return {"answer": answer}
