"""FastAPI entry point."""
import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

from .database import Base, engine
from . import models  # noqa: F401  — register models on Base
from .routes import router

load_dotenv()

# Create tables on startup. For production, switch to Alembic migrations.
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="MedRelay API",
    description="AI-first CRM backend for HCP interactions.",
    version="0.1.0",
)

origins = [
    o.strip()
    for o in os.getenv("CORS_ORIGINS", "http://localhost:5173").split(",")
    if o.strip()
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)


@app.get("/")
def root():
    return {"service": "MedRelay API", "docs": "/docs"}
