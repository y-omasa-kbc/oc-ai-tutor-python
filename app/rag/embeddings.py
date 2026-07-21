from functools import lru_cache

from sentence_transformers import SentenceTransformer

from app.rag.config import EMBEDDING_MODEL


@lru_cache(maxsize=1)
def get_embedding_model() -> SentenceTransformer:
    return SentenceTransformer(EMBEDDING_MODEL)


def _encode(texts: list[str]) -> list[list[float]]:
    model = get_embedding_model()
    vectors = model.encode(texts, normalize_embeddings=True, convert_to_numpy=True)
    return vectors.tolist()


def embed_texts(texts: list[str]) -> list[list[float]]:
    return _encode(["passage: " + t for t in texts])


def embed_query(text: str) -> list[float]:
    return _encode(["query: " + text])[0]
