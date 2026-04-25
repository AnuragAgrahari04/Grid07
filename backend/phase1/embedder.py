"""
Embedding model wrapper.
Uses sentence-transformers (runs locally).
"""

import os

# Keep transformers on torch-only path to avoid tf/keras runtime conflicts.
os.environ.setdefault("TRANSFORMERS_NO_TF", "1")

from sentence_transformers import SentenceTransformer

from core.config import settings
from core.logger import log

_model: SentenceTransformer | None = None


def get_model() -> SentenceTransformer:
    global _model
    if _model is None:
        log.info(f"Loading embedding model: {settings.EMBEDDING_MODEL}")
        _model = SentenceTransformer(settings.EMBEDDING_MODEL)
        dim = _model.get_sentence_embedding_dimension()
        log.success(f"Embedding model loaded. Dimension: {dim}")
    return _model


def embed_text(text: str) -> list[float]:
    model = get_model()
    vector = model.encode(text, convert_to_numpy=True)
    return vector.tolist()


def embed_batch(texts: list[str]) -> list[list[float]]:
    model = get_model()
    vectors = model.encode(texts, convert_to_numpy=True, batch_size=8)
    return vectors.tolist()
