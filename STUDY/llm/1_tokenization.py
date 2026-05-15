from transformers import AutoTokenizer

tokenizer = AutoTokenizer.from_pretrained("gpt2")

text = ["I love FastAPI and MongoDB.", "BidActionHandler", "Bid Action Handler", '{"status": "declined"}']

for i in text:
    tokens = tokenizer.encode(text)
    print(tokens," ", len(tokens))