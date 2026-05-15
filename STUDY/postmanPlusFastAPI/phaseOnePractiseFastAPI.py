from fastapi import FastAPI

app = FastAPI()

'''SINGLE FUNCTIONS'''
# @app.get("/")
# def root():
#     return {
#         "message" : "FastAPI is running"
#     }


'''MULTIPLE FUNCTIONS'''
# @app.get("/")
# def root():
#     return {"message": "Home"}

# @app.get("/users")
# def get_users():
#     return ["Alice", "Bob"]

# @app.get("/health")
# def health():
#     return {"status": "ok"}


users = []

@app.post("/users")
def create_user(name:str, age:int):
    user = {"name":name, "age":age}
    users.append(user)
    return users

@app.get("/users")
def get_users():
    return users


'''
2️⃣ How to test using Swagger (UI)

Open your browser and go to:

👉 http://127.0.0.1:8000/docs

Create a user

Click POST /users

Click Try it out

Enter:

name: Rohit
age: 25


Click Execute

✅ User is created

Get users

Click GET /users → Execute

You’ll see:

[
  {
    "name": "Rohit",
    "age": 25
  }
]

3️⃣ Create users using code (no Swagger)

Yes — and this is how real systems do it.

Using curl (CLI)
curl -X POST "http://127.0.0.1:8000/users?name=Rohit&age=25"

Using Python (requests)
import requests

url = "http://127.0.0.1:8000/users"
params = {"name": "Rohit", "age": 25}

response = requests.post(url, params=params)
print(response.json())
'''




# query selector
@app.get("/search")
def search_items(q: str, limit: int = 10):
    results = []

    for item in users:
        if q in item["name"]:
            results.append(item)

    return results[:limit]

'''
from fastapi import Query

@app.get("/users")
def get_users(
    q: str | None = None,
    age: int | None = None,
    limit: int = Query(10, ge=1, le=50),
    offset: int = Query(0, ge=0)
):
    results = users

    # searching
    if q:
        results = [
            u for u in results
            if q.lower() in u["name"].lower()
        ]

    # filtering
    if age is not None:
        results = [
            u for u in results
            if u["age"] == age
        ]

    # pagination
    return results[offset : offset + limit]
'''


# path parameter

@app.get("/users/{user_id}")
def get_user(user_id: int):
    # Check if the user exists in the list
    if user_id < 0 or user_id >= len(users):
        return {"error": "User not found"}
    
    return users[user_id]
