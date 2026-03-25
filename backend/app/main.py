from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.routes.finance_routes import router as finance_router

app = FastAPI(title=settings.app_name, version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def health() -> dict[str, str]:
    return {"status": "ok", "service": settings.app_name}


app.include_router(finance_router, prefix=settings.api_prefix)
