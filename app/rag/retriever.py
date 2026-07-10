import json
from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path

import numpy as np

from app.rag.config import (
    CHUNKS_PATH,
    EMBEDDINGS_PATH,
    RETRIEVAL_TOP_K,
)
from app.rag.embeddings import embed_query


@dataclass
class RetrievedChunk:
    source: str
    text: str
    score: float


@lru_cache(maxsize=1)
def _load_chunks() -> tuple[dict, ...]:
    if not CHUNKS_PATH.exists():
        raise FileNotFoundError(
            f"インデックスが見つかりません: {CHUNKS_PATH}\n"
            "`python -m app.data.index` を実行してインデックスを生成してください。"
        )
    with CHUNKS_PATH.open(encoding="utf-8") as f:
        chunks = json.load(f)
    return tuple(chunks)


@lru_cache(maxsize=1)
def _load_embeddings() -> np.ndarray:
    if not EMBEDDINGS_PATH.exists():
        raise FileNotFoundError(
            f"埋め込みが見つかりません: {EMBEDDINGS_PATH}\n"
            "`python -m app.data.index` を実行してインデックスを生成してください。"
        )
    return np.load(EMBEDDINGS_PATH)


def search(query: str, top_k: int | None = None) -> list[RetrievedChunk]:
    k = top_k or RETRIEVAL_TOP_K
    chunks = _load_chunks()
    embeddings = _load_embeddings()
    if len(chunks) == 0:
        return []

    query_vec = np.array(embed_query(query), dtype=np.float32)
    scores = embeddings @ query_vec
    top_indices = np.argsort(scores)[::-1][:k]

    return [
        RetrievedChunk(source=chunks[i]["source"], text=chunks[i]["text"], score=float(scores[i]))
        for i in top_indices
    ]
