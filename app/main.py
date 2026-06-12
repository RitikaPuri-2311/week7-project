from fastapi import FastAPI

from app.database import engine, Base
import app.models

from app.routes.user import router as user_router
from app.routes.analytics import router as analytics_router

app = FastAPI()

Base.metadata.create_all(bind=engine)

app.include_router(user_router)
app.include_router(analytics_router)

@app.get("/")
def home():
    return {"message": "FastAPI Running"}