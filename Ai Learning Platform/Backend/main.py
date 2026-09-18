from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from database import engine, Base
import models

from routes.auth_routes import router as auth_router
from routes.user_routes import router as user_router

from routes.quiz_routes import router as quiz_router


# Create database tables
Base.metadata.create_all(bind=engine)


app = FastAPI(
    title="KarmAI Backend",
    description="Backend API for the KarmAI Learning Platform",
    version="1.0.0"
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Register routes
app.include_router(auth_router)
app.include_router(user_router)
app.include_router(quiz_router)


@app.get("/")
def root():
    return {
        "message": "KarmAI Backend is running"
    }


@app.get("/api/v1/health")
def health_check():
    return {
        "status": "healthy"
    }