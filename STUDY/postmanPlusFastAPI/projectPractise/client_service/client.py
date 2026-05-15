import requests

BASE_URL = "http://localhost:8000"

def create_user():
    payload = {
        "name": "Rohit",
        "email": "rohit3@gmail.com"
    }

    response = requests.post(
        f"{BASE_URL}/users/",
        json=payload,
        timeout=5
    )

    response.raise_for_status()
    return response.json()

def get_all_users():
    response = requests.get(
        f"{BASE_URL}/users/",
        timeout=5
    )
    response.raise_for_status()
    return response.json()

def get_user_by_id(user_id):
    response = requests.get(
        f"{BASE_URL}/users/{user_id}",
        timeout=5
    )
    response.raise_for_status()
    return response.json()

if __name__ == "__main__":
    user = create_user()
    print("Created User:", user)

    users = get_all_users()
    print("All Users:", users)

    user_data = get_user_by_id(user["id"])
    print("Fetched Single User:", user_data)



if __name__ == "__main__":
    user_id = "698451b4828befb42ef8cef3"  # example ObjectId string

    user = get_user_by_id(user_id)
    print("Fetched user:", user)
