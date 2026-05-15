# # # from langchain.agents import initialize_agent
# # # from langchain.agents import AgentType  ---> depriicated
# # from langchain.agents import create_react_agent, AgentExecutor

# # from services.langchain_llm import CerebrasRunnable
# # from langchain_core.tools import Tool

# # from langchain_core.runnables import RunnableParallel, RunnableLambda
# # from langchain_core.output_parsers import StrOutputParser
# # from langchain_core.prompts import ChatPromptTemplate
# # from services.faiss_service import FAISSService
# # from services.bm25_service import BM25Service
# # from services.rerank_service import RerankService
# # from services.embedding_service import EmbeddingService

# # def load_documents(path):
# #     with open(path, "r", encoding="utf-8") as f:
# #         return [line.strip() for line in f.readlines() if line.strip()]
# # documents = load_documents("data/documents.txt")

# # faiss = FAISSService(documents)
# # bm25 = BM25Service(documents)
# # reranker = RerankService()
# # embedder = EmbeddingService()

# # def faiss_retriever(x):
# #     query = x["question"]
# #     query_embedding = embedder.embed(query)
# #     return faiss.search(query_embedding, k=5)


# # def bm25_retriever(x):
# #     return bm25.search(x["question"], k=5)


# # def merge_results(x):
# #     combined = list(set(x["faiss"] + x["bm25"]))
# #     return {
# #         "question": x["question"],
# #         "docs": combined
# #     }


# # def rerank_results(x):
# #     ranked = reranker.rerank(x["question"], x["docs"])
# #     return {
# #         "question": x["question"],
# #         "context": "\n\n".join(ranked[:3])
# #     }

# # prompt = ChatPromptTemplate.from_template(
# # """
# # Use ONLY the context below to answer.

# # Context:
# # {context}

# # Question:
# # {question}

# # Answer:
# # """
# # )

# # parser = StrOutputParser()
# # llm = CerebrasRunnable()


# # def calculator_tool(input):
# #     try:
# #         return str(eval(input))
# #     except:
# #         return "Error in calculation"
    
# # def rag_tool_func(query: str):
# #     return chain.invoke({"question": query})

# # chain = (
# #     RunnableParallel({
# #         "question": lambda x: x["question"],
# #         "faiss": RunnableLambda(faiss_retriever),
# #         "bm25": RunnableLambda(bm25_retriever)
# #     })
# #     | RunnableLambda(merge_results)
# #     | RunnableLambda(rerank_results)
# #     | prompt
# #     | llm
# #     | parser
# # )

# # calculator = Tool(
# #     name="Calculator",
# #     func=calculator_tool,
# #     description="Useful for solving math expressions"
# # )
# # rag_tool = Tool(
# #     name="KnowledgeBase",
# #     func=rag_tool_func,
# #     description="Answer questions using internal knowledge base"
# # )

# # # agent = initialize_agent(
# # #     tools=[calculator, rag_tool],
# # #     llm=llm,
# # #     agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
# # #     verbose=True
# # # )
# # tools = [calculator, rag_tool]
# # from langchain import hub
# # react_prompt = hub.pull("hwchase17/react")

# # agent = create_react_agent(
# #     llm=llm,
# #     tools=tools,
# #     prompt=react_prompt
# # )

# # agent_executor = AgentExecutor(
# #     agent=agent,
# #     tools=tools,
# #     verbose=True
# # )



# # if __name__ == "__main__":
# #     while True:
# #         query = input("\nAsk: ")
# #         # response = agent.run(query)
# #         # print("\nAnswer:", response)
# #         response = agent_executor.invoke({"input": query})
# #         print("\nAnswer:", response["output"])





# # from langchain.agents import create_agent
# # from langchain_core.tools import tool

# # from services.langchain_llm import CerebrasRunnable
# # from langchain_core.runnables import RunnableParallel, RunnableLambda
# # from langchain_core.output_parsers import StrOutputParser
# # from langchain_core.prompts import ChatPromptTemplate

# # from services.faiss_service import FAISSService
# # from services.bm25_service import BM25Service
# # from services.rerank_service import RerankService
# # from services.embedding_service import EmbeddingService

# # import math


# # # -----------------------------
# # # Load Documents
# # # -----------------------------
# # def load_documents(path):
# #     with open(path, "r", encoding="utf-8") as f:
# #         return [line.strip() for line in f.readlines() if line.strip()]


# # documents = load_documents("data/documents.txt")


# # # -----------------------------
# # # Initialize Services
# # # -----------------------------
# # faiss = FAISSService()
# # bm25 = BM25Service(documents)
# # reranker = RerankService()
# # embedder = EmbeddingService()
# # llm = CerebrasRunnable()


# # # -----------------------------
# # # Retrieval Functions
# # # -----------------------------
# # def faiss_retriever(x):
# #     query = x["question"]
# #     query_embedding = embedder.embed(query)
# #     return faiss.search(query_embedding, k=5)


# # def bm25_retriever(x):
# #     return bm25.search(x["question"], k=5)


# # def merge_results(x):
# #     combined = list(set(x["faiss"] + x["bm25"]))
# #     return {
# #         "question": x["question"],
# #         "docs": combined
# #     }


# # def rerank_results(x):
# #     ranked = reranker.rerank(x["question"], x["docs"])
# #     return {
# #         "question": x["question"],
# #         "context": "\n\n".join(ranked[:3])
# #     }


# # # -----------------------------
# # # Prompt + Parser
# # # -----------------------------
# # prompt = ChatPromptTemplate.from_template(
# #     """
# # Use ONLY the context below to answer.

# # Context:
# # {context}

# # Question:
# # {question}

# # Answer:
# # """
# # )

# # parser = StrOutputParser()


# # # -----------------------------
# # # RAG Chain (DEFINE BEFORE TOOLS ✅)
# # # -----------------------------
# # chain = (
# #     RunnableParallel({
# #         "question": lambda x: x["question"],
# #         "faiss": RunnableLambda(faiss_retriever),
# #         "bm25": RunnableLambda(bm25_retriever)
# #     })
# #     | RunnableLambda(merge_results)
# #     | RunnableLambda(rerank_results)
# #     | prompt
# #     | llm
# #     | parser
# # )


# # # -----------------------------
# # # Tools (v1 style ✅)
# # # -----------------------------
# # @tool
# # def calculator(query: str) -> str:
# #     """Useful for solving math expressions"""
# #     try:
# #         return str(eval(query, {"__builtins__": None}, {"math": math}))
# #     except:
# #         return "Error in calculation"


# # @tool
# # def knowledge_base(question: str) -> str:
# #     """Use this to answer questions about vector databases, embeddings, FAISS, BM25, or any stored documents"""
# #     return chain.invoke({"question": question})


# # tools = [calculator, knowledge_base]


# # # -----------------------------
# # # Agent (LangChain v1 ✅)
# # # -----------------------------
# # agent = create_agent(
# #     model=llm,
# #     tools=tools,
# #     system_prompt="You are a helpful assistant. Use tools when necessary."
# # )


# # # -----------------------------
# # # Run Loop
# # # -----------------------------
# # # if __name__ == "__main__":
# # #     while True:
# # #         query = input("\nAsk: ")

# # #         response = agent.invoke({
# # #             "messages": [
# # #                 {"role": "user", "content": query}
# # #             ]
# # #         })

# # #         print("\nAnswer:", response["messages"][-1].content)


# # if __name__ == "__main__":
# #     while True:
# #         query = input("\nAsk: ")

# #         # simple routing logic
# #         if any(op in query for op in ["+", "-", "*", "/"]):
# #             response = calculator.invoke(query)
# #         else:
# #             response = knowledge_base.invoke(query)

# #         print("\nAnswer:", response)






# from langchain_core.tools import tool
# from services.langchain_llm import CerebrasRunnable
# from langchain_core.runnables import RunnableParallel, RunnableLambda
# from langchain_core.output_parsers import StrOutputParser
# from langchain_core.prompts import ChatPromptTemplate

# from services.faiss_service import FAISSService
# from services.bm25_service import BM25Service
# from services.rerank_service import RerankService
# from services.embedding_service import EmbeddingService

# import math

# # -----------------------------
# # Load Documents
# # -----------------------------
# def load_documents(path):
#     with open(path, "r", encoding="utf-8") as f:
#         return [line.strip() for line in f.readlines() if line.strip()]

# documents = load_documents("data/documents.txt")

# # -----------------------------
# # Initialize Services
# # -----------------------------
# faiss = FAISSService()
# bm25 = BM25Service(documents)
# reranker = RerankService()
# embedder = EmbeddingService()
# llm = CerebrasRunnable()

# # -----------------------------
# # Retrieval Functions
# # -----------------------------
# def faiss_retriever(x):
#     query = x["question"]
#     query_embedding = embedder.embed(query)
#     return faiss.search(query_embedding, k=5)

# def bm25_retriever(x):
#     return bm25.search(x["question"], k=5)

# def merge_results(x):
#     combined = list(set(x["faiss"] + x["bm25"]))
#     return {
#         "question": x["question"],
#         "docs": combined
#     }

# def rerank_results(x):
#     ranked = reranker.rerank(x["question"], x["docs"])
#     return {
#         "question": x["question"],
#         "context": "\n\n".join(ranked[:3])
#     }

# # -----------------------------
# # Prompt + Parser
# # -----------------------------
# prompt = ChatPromptTemplate.from_template(
#     """
# Use ONLY the context below to answer.

# Context:
# {context}

# Question:
# {question}

# Answer:
# """
# )
# parser = StrOutputParser()

# # -----------------------------
# # RAG Chain
# # -----------------------------
# chain = (
#     RunnableParallel({
#         "question": lambda x: x["question"],
#         "faiss": RunnableLambda(faiss_retriever),
#         "bm25": RunnableLambda(bm25_retriever)
#     })
#     | RunnableLambda(merge_results)
#     | RunnableLambda(rerank_results)
#     | prompt
#     | llm
#     | parser
# )

# # -----------------------------
# # Tools
# # -----------------------------
# @tool
# def calculator(query: str) -> str:
#     """Solve math expressions safely."""
#     try:
#         return str(eval(query))
#     except:
#         return "Error in calculation"

# @tool
# def knowledge_base(query: str) -> str:
#     """Answer questions using your RAG knowledge base."""
#     return chain.invoke({"question": query})

# TOOLS = {
#     "calculator": calculator,
#     "knowledge_base": knowledge_base
# }

# # -----------------------------
# # Agent-Like Function
# # -----------------------------
# def agent_like(query: str) -> str:
#     """
#     Routes queries to the appropriate tool.
#     - Math expressions -> calculator
#     - Everything else -> RAG knowledge base
#     """
#     math_ops = ["+", "-", "*", "/"]

#     if any(op in query for op in math_ops):
#         return TOOLS["calculator"].invoke(query)
#     else:
#         return TOOLS["knowledge_base"].invoke(query)

# # -----------------------------
# # Run Loop
# # -----------------------------
# if __name__ == "__main__":
#     print("Agent is ready. Type your questions below (type 'exit' to quit).")
#     while True:
#         query = input("\nAsk: ")
#         if query.lower() in ["exit", "quit"]:
#             break

#         response = agent_like(query)
#         print("\nAnswer:", response)










from langchain.agents import create_agent
from langchain_core.tools import tool

from langchain_core.runnables import RunnableParallel, RunnableLambda
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate

from services.langchain_llm import CerebrasRunnable
from services.faiss_service import FAISSService
from services.bm25_service import BM25Service
from services.rerank_service import RerankService
from services.embedding_service import EmbeddingService

import math

# -----------------------------
# Load Documents
# -----------------------------
def load_documents(path):
    with open(path, "r", encoding="utf-8") as f:
        return [line.strip() for line in f.readlines() if line.strip()]

documents = load_documents("data/documents.txt")

# -----------------------------
# Initialize Services
# -----------------------------
faiss = FAISSService(documents)   # ✅ FIXED
bm25 = BM25Service(documents)
reranker = RerankService()
embedder = EmbeddingService()
llm = CerebrasRunnable()          # must return STRING

# -----------------------------
# Retrieval Functions
# -----------------------------
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

def rerank_results(x):
    ranked = reranker.rerank(x["question"], x["docs"])
    return {
        "question": x["question"],
        "context": "\n\n".join(ranked[:3])
    }

# -----------------------------
# Prompt + Parser
# -----------------------------
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

parser = StrOutputParser()

# -----------------------------
# RAG Chain
# -----------------------------
chain = (
    RunnableParallel({
        "question": lambda x: x["question"],
        "faiss": RunnableLambda(faiss_retriever),
        "bm25": RunnableLambda(bm25_retriever)
    })
    | RunnableLambda(merge_results)
    | RunnableLambda(rerank_results)
    | prompt
    | llm
    | parser
)

# -----------------------------
# Tools (Structured ✅)
# -----------------------------
@tool
def calculator(query: str) -> str:
    """Use this for math calculations like 2+2, 10*5, etc."""
    try:
        return str(eval(query, {"__builtins__": None}, vars(math)))
    except:
        return "Error in calculation"

@tool
def knowledge_base(question: str) -> str:
    """Use this for answering questions about vector databases, embeddings, FAISS, BM25 or stored documents."""
    return chain.invoke({"question": question})

tools = [calculator, knowledge_base]

# -----------------------------
# Agent (Modern LangChain ✅)
# -----------------------------
agent = create_agent(
    model=llm,
    tools=tools,
    system_prompt="""
You are a helpful AI assistant.

- Use calculator for math problems
- Use knowledge_base for factual or technical questions
- If unsure, use knowledge_base
"""
)

# -----------------------------
# Run Loop
# -----------------------------
if __name__ == "__main__":
    print("🚀 Agent is ready. Type 'exit' to quit.\n")

    while True:
        query = input("Ask: ")

        if query.lower() in ["exit", "quit"]:
            break

        response = agent.invoke({
            "messages": [
                {"role": "user", "content": query}
            ]
        })

        print("\nAnswer:", response["messages"][-1].content)