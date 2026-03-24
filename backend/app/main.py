"""FastAPI application entrypoint for FinGuru backend."""

from contextlib import asynccontextmanager
import os
import sys
from pathlib import Path

from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Allow direct execution via: python backend/app/main.py
BACKEND_DIR = Path(__file__).resolve().parents[1]
if str(BACKEND_DIR) not in sys.path:
    sys.path.insert(0, str(BACKEND_DIR))

from app.routes import agent_routes, chat_routes, financial_analysis_routes, user_routes


# Load environment from backend/.env if present.
load_dotenv(BACKEND_DIR / ".env")


@asynccontextmanager
async def lifespan(_: FastAPI):
    """Handle startup/shutdown lifecycle events."""
    print("FinGuru backend starting...")
    yield
    print("FinGuru backend shutting down...")


app = FastAPI(
    title="FinGuru API",
    description="AI-powered personal finance mentor API",
    version="1.0.0",
    lifespan=lifespan,
)


frontend_url = os.getenv("FRONTEND_URL", "http://localhost:3000")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[frontend_url],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(user_routes.router, prefix="/api/users", tags=["Users"])
app.include_router(
    financial_analysis_routes.router,
    prefix="/api/financial",
    tags=["Financial Analysis"],
)
app.include_router(agent_routes.router, prefix="/api/agents", tags=["AI Agents"])
app.include_router(chat_routes.router, prefix="/api/chat", tags=["Chat"])


@app.get("/", tags=["Health"])
async def root():
    return {
        "message": "Welcome to FinGuru API",
        "version": "1.0.0",
        "status": "active",
    }


@app.get("/health", tags=["Health"])
async def health_check():
    return {"status": "healthy", "service": "FinGuru Backend"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
