"""
Clio RAG Service — engine.py
LlamaIndex + Chroma + FAISS core logic.
Embedding provider auto-detected from env or runtime probe.
"""

import asyncio
import logging
import os
from pathlib import Path
from urllib.parse import urlparse

import httpx
import chromadb
from llama_index.core import (
    SimpleDirectoryReader,
    StorageContext,
    VectorStoreIndex,
)
from llama_index.vector_stores.chroma import ChromaVectorStore

logger = logging.getLogger(__name__)

SOURCES_DIR = Path(os.getenv("SOURCES_DIR", "/data/sources"))
CHROMA_DIR = Path(os.getenv("CHROMA_DIR", "/data/chroma_db"))
COLLECTION_NAME = os.getenv("CHROMA_COLLECTION", "clio_knowledge")

EMBEDDING_BASE_URL = os.getenv("EMBEDDING_BASE_URL", "")
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "nomic-embed-text")

PROBE_TARGETS = [
    ("ollama", "http://host.docker.internal:11434/api/tags"),
    ("mlx",    "http://host.docker.internal:1234/v1/models"),
]


async def _probe_embedding_url() -> str:
    async with httpx.AsyncClient(timeout=3.0) as client:
        for name, url in PROBE_TARGETS:
            try:
                r = await client.get(url)
                if r.status_code == 200:
                    logger.info(f"Auto-detected embedding provider: {name} at {url}")
                    p = urlparse(url)
                    return f"{p.scheme}://{p.netloc}"
            except Exception:
                continue
    raise RuntimeError(
        "No embedding provider found. Set EMBEDDING_BASE_URL or start Ollama/MLX-LM on the host."
    )


def _build_embed_model(base_url: str):
    from llama_index.embeddings.ollama import OllamaEmbedding
    return OllamaEmbedding(model_name=EMBEDDING_MODEL, base_url=base_url)


class RagEngine:
    def __init__(self):
        self.index: VectorStoreIndex = None
        self.embed_model = None

    async def init(self):
        base_url = EMBEDDING_BASE_URL.strip()
        if not base_url:
            logger.info("EMBEDDING_BASE_URL not set — probing host...")
            base_url = await _probe_embedding_url()
        else:
            logger.info(f"Using configured EMBEDDING_BASE_URL: {base_url}")

        self.embed_model = _build_embed_model(base_url)

        CHROMA_DIR.mkdir(parents=True, exist_ok=True)
        chroma_client = chromadb.PersistentClient(path=str(CHROMA_DIR))
        chroma_collection = chroma_client.get_or_create_collection(COLLECTION_NAME)
        vector_store = ChromaVectorStore(chroma_collection=chroma_collection)
        storage_context = StorageContext.from_defaults(vector_store=vector_store)

        SOURCES_DIR.mkdir(parents=True, exist_ok=True)
        source_files = [f for f in SOURCES_DIR.rglob("*") if f.is_file()]

        if source_files:
            logger.info(f"Indexing {len(source_files)} file(s) from {SOURCES_DIR}")
            documents = SimpleDirectoryReader(str(SOURCES_DIR), recursive=True).load_data()
            self.index = VectorStoreIndex.from_documents(
                documents,
                storage_context=storage_context,
                embed_model=self.embed_model,
            )
        else:
            logger.warning(f"No source files found in {SOURCES_DIR}. Index is empty.")
            self.index = VectorStoreIndex.from_vector_store(
                vector_store,
                embed_model=self.embed_model,
            )

    async def query(self, query_text: str, top_k: int = 5) -> list[dict]:
        if self.index is None:
            raise RuntimeError("Index not initialised")
        retriever = self.index.as_retriever(similarity_top_k=top_k)
        nodes = await asyncio.get_event_loop().run_in_executor(
            None, retriever.retrieve, query_text
        )
        return [
            {
                "text": node.get_content(),
                "score": node.score,
                "source": node.metadata.get("file_name", "unknown"),
            }
            for node in nodes
        ]

    async def ingest(self) -> int:
        source_files = [f for f in SOURCES_DIR.rglob("*") if f.is_file()]
        if not source_files:
            logger.warning("No files to ingest.")
            return 0

        documents = await asyncio.get_event_loop().run_in_executor(
            None,
            lambda: SimpleDirectoryReader(str(SOURCES_DIR), recursive=True).load_data(),
        )

        chroma_client = chromadb.PersistentClient(path=str(CHROMA_DIR))
        chroma_collection = chroma_client.get_or_create_collection(COLLECTION_NAME)
        vector_store = ChromaVectorStore(chroma_collection=chroma_collection)
        storage_context = StorageContext.from_defaults(vector_store=vector_store)

        self.index = await asyncio.get_event_loop().run_in_executor(
            None,
            lambda: VectorStoreIndex.from_documents(
                documents,
                storage_context=storage_context,
                embed_model=self.embed_model,
            ),
        )

        logger.info(f"Ingested {len(source_files)} file(s).")
        return len(source_files)
