from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.health import router as health_router
from app.config import get_settings
from app.api.v1 import router as v1_router
from app.api.errors import register_errors

app = FastAPI(title="TANCE API", version="0.1.0", description="摊策 · 本地开发环境")
app.add_middleware(
    CORSMiddleware,
    allow_origins=get_settings().cors_origins,
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(health_router, prefix="/api")
app.include_router(v1_router)
register_errors(app)


@app.get("/api/v1/health", tags=["Health"])
def v1_health() -> dict[str, str]:
    return {"status": "ok"}
