from fastapi import FastAPI, Response
from fastapi.middleware.cors import CORSMiddleware

try:
    from app.config import settings
    from app.routes.finance_routes import router as finance_router
except ModuleNotFoundError:
    import sys
    from pathlib import Path

    # Supports running as: python backend/app/main.py
    backend_root = Path(__file__).resolve().parents[1]
    if str(backend_root) not in sys.path:
        sys.path.insert(0, str(backend_root))

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


@app.get("/favicon.ico", include_in_schema=False)
def favicon() -> Response:
    # Return empty favicon response so browser request does not show 404 in logs.
    return Response(status_code=204)


app.include_router(finance_router, prefix=settings.api_prefix)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=True)
