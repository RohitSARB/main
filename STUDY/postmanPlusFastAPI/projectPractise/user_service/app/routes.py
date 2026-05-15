from fastapi import APIRouter, HTTPException
from bson import ObjectId
from app.database import user_collection
from app.schemas import UserCreate, UserResponse

router = APIRouter(prefix="/users", tags=["Users"])

@router.post("/", response_model=UserResponse)
async def create_user(user: UserCreate):
    existing = await user_collection.find_one({"email": user.email})
    if existing:
        raise HTTPException(status_code=400, detail="User already exists")

    result = await user_collection.insert_one(user.dict())
    return {
        "id": str(result.inserted_id),
        **user.dict()
    }

@router.get("/{user_id}", response_model=UserResponse)
async def get_user(user_id: str):
    user = await user_collection.find_one({"_id": ObjectId(user_id)})
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return {
        "id": str(user["_id"]),
        "name": user["name"],
        "email": user["email"]
    }

@router.get("/", response_model=list[UserResponse])
async def get_users():
    users = []
    async for u in user_collection.find():
        users.append({
            "id": str(u["_id"]),
            "name": u["name"],
            "email": u["email"]
        })
    return users
