from assistant import Assistant

docs = open("data/documents.txt").read().split("\n\n")

assistant = Assistant(docs)

while True:
    q = input("You: ")

    if q == "exit":
        break

    print("Assistant: ", assistant.chat(q))