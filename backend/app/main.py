from fastapi import FastAPI

from app.api.health import router as health_router
from app.api.qf import router as qf_router

app = FastAPI(
    title="Cairn API",
    description="REST API for the Cairn quadratic funding platform.",
    version="0.1.0",
)

app.include_router(health_router)
app.include_router(qf_router)
