from langchain_core.runnables import RunnableLambda
from services.faiss_service import FAISSService
from services.bm25_service import BM25Service
from services.rerank_service import RerankService
from services.embedding_service import EmbeddingService

def load_documents(path):
    with open(path, "r", encoding="utf-8") as f:
        return [line.strip() for line in f.readlines() if line.strip()]
documents = load_documents("data/documents.txt")

faiss = FAISSService()
bm25 = BM25Service(documents)
reranker = RerankService()
embedder = EmbeddingService()


def faiss_retriever(x):
    query = x["question"]
    query_embedding = embedder.embed(query)
    return faiss.search(query_embedding, k=5)

def bm25_retriever(x):
    return bm25.search(x["question"], k=5)

def merge_results(x):
    combined = list(set(x["faiss"] + x["bm25"]))
    return {
        "question": x["question"],
        "docs": combined
    }

def rerank(x):
    ranked = reranker.rerank(x["question"], x["docs"])
    return {
        "question": x["question"],
        "context": "\n\n".join(ranked[:3])
    }

from langchain_core.prompts import ChatPromptTemplate

prompt = ChatPromptTemplate.from_template(
"""
You are a helpful assistant.

Use ONLY the context below to answer.

Context:
{context}

Question:
{question}

Answer:
"""
)

from langchain_core.runnables import RunnableParallel, RunnableLambda
from langchain_core.output_parsers import StrOutputParser

from services.langchain_llm import CerebrasRunnable

llm = CerebrasRunnable()
parser = StrOutputParser()

chain = (

    # Step 1: Parallel Retrieval
    RunnableParallel({
        "question": lambda x: x["question"],
        "faiss": RunnableLambda(faiss_retriever),
        "bm25": RunnableLambda(bm25_retriever)
    })

    # Step 2: Merge
    | RunnableLambda(merge_results)

    # Step 3: Rerank
    | RunnableLambda(rerank)

    # Step 4: Prompt
    | prompt

    # Step 5: LLM
    | llm

    # Step 6: Parse output
    | parser
)



if __name__ == "__main__":
    result = chain.invoke({
        "question": "Explain vector databases in RAG systems"
    })

    print(result)