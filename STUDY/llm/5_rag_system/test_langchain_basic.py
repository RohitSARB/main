# from langchain_core.prompts import ChatPromptTemplate
# from services.langchain_llm import CerebrasRunnable


# llm = CerebrasRunnable()

# prompt = ChatPromptTemplate.from_template(
#     "Explain {topic} in simple terms."
# )

# chain = prompt | llm

# query = str(input("Enter ur query: "))

# result = chain.invoke({
#     # "topic": "vector databases"
#     "topic": query
# })

# print(result)



from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import (
    RunnableLambda,
    RunnableParallel,
    RunnablePassthrough,
    RunnableBranch
)

from services.langchain_llm import CerebrasRunnable


# ---------------------------
# 1. LLM + Parser
# ---------------------------
llm = CerebrasRunnable()
parser = StrOutputParser()


# ---------------------------
# 2. Prompt
# ---------------------------
prompt = ChatPromptTemplate.from_template(
    "Context: {context}\n\nQuestion: {question}\n\nAnswer:"
)


# ---------------------------
# 3. Preprocess
# ---------------------------
def preprocess(x):
    return {
        "question": x["question"].strip().lower()
    }


# ---------------------------
# 4. Fake Retriever
# ---------------------------
def retrieve_context(x):
    return "Vector databases store embeddings and allow similarity search."


# ---------------------------
# 5. Debug Logger
# ---------------------------
def debug(x):
    print("\nDEBUG INPUT:\n", x)
    return x


# ---------------------------
# 6. Simple vs Complex Logic
# ---------------------------
def is_complex(x):
    q = x["question"]
    return len(q.split()) > 5   # simple heuristic


# ---------------------------
# 7. Branch Pipelines
# ---------------------------

# SIMPLE FLOW (no context)
simple_chain = (
    RunnablePassthrough.assign(context=lambda x: "")
    | prompt
    | llm
    | parser
)

# COMPLEX FLOW (with context)
complex_chain = (
    RunnablePassthrough.assign(context=RunnableLambda(retrieve_context))
    | prompt
    | llm
    | parser
)


# ---------------------------
# 8. Main Chain (ALL CONCEPTS)
# ---------------------------
chain = (
    RunnableLambda(preprocess)   # clean input
    | RunnableLambda(debug)      # debug
    | RunnableBranch(
        (is_complex, complex_chain),   # if True
        simple_chain                  # default
    )
)


# ---------------------------
# 9. Run
# ---------------------------
if __name__ == "__main__":

    question = input("Ask something: ")

    result = chain.invoke({
        "question": question
    })

    print("\nFINAL ANSWER:\n", result)