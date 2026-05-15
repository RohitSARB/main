from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()
users = []
# class UserCreate(BaseModel):
#     name: str
#     email: str
#     age: int

# @app.post("/users")
# def create_user(user: UserCreate):
#     return {
#         "msg": "User Created",
#         "user": user
#     }




# Field-Level Validation (Expert Habit)
from pydantic import BaseModel, EmailStr, Field


class Address(BaseModel):
    city: str
    state: str

class UserCreate(BaseModel):
    name: str = Field(..., min_length=3)
    email: EmailStr
    age: int = Field(..., ge=18, le=100)
    address: Address

@app.post("/users")
# def create_user(user: UserCreate):
#     return {
#         "msg": "User Created",
#         "user": user
#     }
def create_user(user: UserCreate):
    users.append(user)
    return user

@app.get("/users/{user_id}")
def get_users(userId: int):
    return users[userId]



'''
Response Models (Clean APIs)

Never return raw objects in production.

class UserResponse(BaseModel):
    name: str
    email: str

@app.post("/users", response_model=UserResponse)
def create_user(user: UserCreate):
    return user


Age is hidden automatically. '''

'''
Production-Grade Pattern (Recommended)
Separate models clearly
class UserCreate(BaseModel):
    name: str = Field(..., min_length=3)
    email: EmailStr
    age: int = Field(..., ge=18, le=100)

class UserResponse(BaseModel):
    name: str
    email: EmailStr

@app.post("/users", response_model=UserResponse, status_code=201)
def create_user(user: UserCreate):
    # save user to DB here
    return user
'''


# Request models = what clients send
# Response models = what clients are allowed to see


'''
Optional Fields & Defaults
from typing import Optional

class ItemCreate(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    is_active: bool = True
'''


