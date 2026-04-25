"""
Grid07 Cognitive Engine - FastAPI Backend.
Exposes Phase 1, 2, and 3 as REST API endpoints.
"""

from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.routes_phase1 import router as phase1_router
from api.routes_phase2 import router as phase2_router
from api.routes_phase3 import router as phase3_router
from core.logger import log
from phase1.vector_store import get_collection


@asynccontextmanager
async def lifespan(app: FastAPI):
    log.info("Grid07 Cognitive Engine starting up...")
    get_collection()
    log.success("All systems ready. Vector store initialized.")
    yield
    log.info("Shutting down...")


app = FastAPI(
    title="Grid07 Cognitive Engine",
    description="AI cognitive loop: vector routing, LangGraph content engine, RAG combat system",
    version="1.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(phase1_router, prefix="/api/phase1", tags=["Phase 1 - Router"])
app.include_router(phase2_router, prefix="/api/phase2", tags=["Phase 2 - Content Engine"])
app.include_router(phase3_router, prefix="/api/phase3", tags=["Phase 3 - Combat Engine"])


@app.get("/api/health")
async def health() -> dict:
    return {"status": "ok", "service": "grid07-cognitive-engine"}
