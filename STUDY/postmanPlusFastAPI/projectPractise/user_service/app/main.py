from fastapi import FastAPI
from app.routes import router
# from projectPractise.user_service.app.routes import router


app = FastAPI(title="User Service")

app.include_router(router)
