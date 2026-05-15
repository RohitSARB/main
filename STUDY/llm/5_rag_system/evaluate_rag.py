# import json
# from services.rag_pipeline import RAGPipeline


# documents = open("data/documents.txt").read().split("\n\n")

# rag = RAGPipeline(documents)


# with open("data/eval_dataset.json") as f:
#     dataset = json.load(f)


# correct = 0

# for item in dataset:

#     question = item["question"]
#     expected = item["expected_answer"]

#     answer = rag.ask(question)

#     print("Question:", question)
#     print("Expected:", expected)
#     print("Answer:", answer)
#     print()

#     if expected.lower() in answer.lower():
#         correct += 1


# score = correct / len(dataset)

# print("Accuracy:", score)





import json

from services.rag_pipeline import RAGPipeline
from services.evaluator_service import EvaluatorService


documents = open("data/documents.txt").read().split("\n\n")

rag = RAGPipeline(documents)

evaluator = EvaluatorService()


with open("data/eval_dataset.json") as f:
    dataset = json.load(f)


for item in dataset:

    question = item["question"]
    expected = item["expected_answer"]

    answer = rag.ask(question)

    evaluation = evaluator.evaluate(question, expected, answer)

    print("Question:", question)
    print("Answer:", answer)
    print("Evaluation:", evaluation)
    print()