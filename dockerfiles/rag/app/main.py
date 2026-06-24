"""
Clio RAG Service — main.py
FastAPI app exposing query and ingest endpoints.
"""

import logging
import os
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from app.engine import RagEngine

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

engine: RagEngine = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    global engine
    logger.info("Initialising RAG engine...")
    engine = RagEngine()
    await engine.init()
    logger.info("RAG engine ready.")
    yield
    logger.info("Shutting down RAG engine.")


app = FastAPI(
    title="Clio RAG Service",
    description="Semantic retrieval over Clio's knowledge corpus.",
    version="0.1.0",
    lifespan=lifespan,
)


class QueryRequest(BaseModel):
    query: str
    top_k: int = 5


class QueryResponse(BaseModel):
    query: str
    results: list[dict]


class IngestResponse(BaseModel):
    status: str
    files_indexed: int


@app.get("/healthz")
async def health():
    return {"status": "ok"}


@app.post("/query", response_model=QueryResponse)
async def query(request: QueryRequest):
    if engine is None:
        raise HTTPException(status_code=503, detail="Engine not ready")
    try:
        results = await engine.query(request.query, request.top_k)
        return QueryResponse(query=request.query, results=results)
    except Exception as e:
        logger.error(f"Query failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/ingest", response_model=IngestResponse)
async def ingest():
    """Re-index all files in the sources directory."""
    if engine is None:
        raise HTTPException(status_code=503, detail="Engine not ready")
    try:
        count = await engine.ingest()
        return IngestResponse(status="ok", files_indexed=count)
    except Exception as e:
        logger.error(f"Ingest failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))
