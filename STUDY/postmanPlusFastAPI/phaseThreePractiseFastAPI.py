'''
Docstring for phaseThreePractiseFastAPI
'''

'''
Use async def by default.
Use def only when the code inside is purely blocking and you cannot make it async.
FastAPI is async-first, but it’s also sync-compatible on purpose.

'''

'''CLEAN PROJECT STRUCTURE'''
# app/
# │── main.py
# │── database.py
# │── models/
# │   └── task.py
# │── routes/
# │   └── task.py
# │── schemas/
# │   └── task.py
# │── config.py


'''
MongoDB Connection (database.py)
from motor.motor_asyncio import AsyncIOMotorClient

MONGO_URL = "mongodb://localhost:27017"

client = AsyncIOMotorClient(MONGO_URL)
db = client["fastapi_db"]

task_collection = db["tasks"]
'''


'''
Pydantic Schemas (schemas/task.py)
from pydantic import BaseModel, Field
from typing import Optional
from bson import ObjectId

class TaskCreate(BaseModel):
    title: str
    description: Optional[str]
    priority: int = Field(..., ge=1, le=5)

class TaskResponse(TaskCreate):
    id: str
'''


'''
Task Routes (routes/task.py)
from fastapi import APIRouter, Depends
from app.schemas.task import TaskCreate, TaskResponse
from app.database import task_collection
from bson import ObjectId

router = APIRouter(prefix="/tasks", tags=["Tasks"])

@router.post("/", response_model=TaskResponse)
async def create_task(task: TaskCreate):
    result = await task_collection.insert_one(task.dict())
    return {
        "id": str(result.inserted_id),
        **task.dict()
    }

@router.get("/", response_model=list[TaskResponse])
async def get_tasks():
    tasks = []
    cursor = task_collection.find()
    async for doc in cursor:
        tasks.append({
            "id": str(doc["_id"]),
            "title": doc["title"],
            "description": doc.get("description"),
            "priority": doc["priority"]
        })
    return tasks
'''



'''
Register Router (main.py)
from fastapi import FastAPI
from app.routes.task import router as task_router

app = FastAPI()

app.include_router(task_router)
'''



'''
ObjectId Handling (Mongo Reality)

Mongo uses _id → ObjectId

Always convert to str:

str(doc["_id"])
Never expose ObjectId directly.



Error Handling (Basic but Clean)
from fastapi import HTTPException

if not task:
    raise HTTPException(status_code=404, detail="Task not found")
'''


'''
Environment Variables (config.py)
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    mongo_url: str = "mongodb://localhost:27017"

settings = Settings()


Use .env later (Phase 4).
'''