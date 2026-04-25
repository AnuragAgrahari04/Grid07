"""
ChromaDB vector store setup.
Runs in-memory and seeds bot personas once.
"""

import chromadb
from chromadb.config import Settings as ChromaSettings
from typing import Any

from core.config import settings
from core.logger import log
from personas.bots import BOT_PERSONAS
from phase1.embedder import embed_batch, embed_text

_client: Any = None
_collection: Any = None


def get_collection() -> Any:
    global _client, _collection

    if _collection is not None:
        return _collection

    log.info("Initializing ChromaDB in-memory vector store...")
    _client = chromadb.Client(ChromaSettings(anonymized_telemetry=False))

    _collection = _client.create_collection(
        name=settings.CHROMA_COLLECTION_NAME,
        metadata={"hnsw:space": "cosine"},
    )

    _seed_personas()
    return _collection


def _seed_personas() -> None:
    log.info("Seeding bot personas into vector store...")

    texts = [bot.persona_text for bot in BOT_PERSONAS]
    ids = [bot.bot_id for bot in BOT_PERSONAS]
    metadatas = [{"name": bot.name, "description": bot.description} for bot in BOT_PERSONAS]

    vectors = embed_batch(texts)

    get_collection().add(ids=ids, embeddings=vectors, documents=texts, metadatas=metadatas)
    log.success(f"Seeded {len(BOT_PERSONAS)} bot personas into ChromaDB")


def query_similar_bots(post_text: str, n_results: int = 3) -> list[dict]:
    collection = get_collection()
    post_vector = embed_text(post_text)

    results = collection.query(
        query_embeddings=[post_vector],
        n_results=n_results,
        include=["metadatas", "distances", "documents"],
    )

    bots_with_scores = []
    for i, bot_id in enumerate(results["ids"][0]):
        distance = results["distances"][0][i]
        similarity = round(1 - distance, 4)
        bots_with_scores.append(
            {
                "bot_id": bot_id,
                "similarity": similarity,
                "metadata": results["metadatas"][0][i],
            }
        )

    return bots_with_scores
