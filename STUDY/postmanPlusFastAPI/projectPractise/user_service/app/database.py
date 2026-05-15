from motor.motor_asyncio import AsyncIOMotorClient
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    mongo_url: str = "mongodb://localhost:27017"

settings = Settings()

client = AsyncIOMotorClient(settings.mongo_url)
db = client["production_db"]
user_collection = db["users"]