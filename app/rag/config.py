import os
from pathlib import Path

from dotenv import load_dotenv

PROJECT_ROOT = Path(__file__).resolve().parents[2]

load_dotenv(PROJECT_ROOT / ".env")


OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY", "")

OPENROUTER_MODEL = os.getenv("OPENROUTER_MODEL", "openai/gpt-4o-mini")

EMBEDDING_MODEL = os.getenv(
    "EMBEDDING_MODEL",
    "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2",
)

RETRIEVAL_TOP_K = int(os.getenv("RETRIEVAL_TOP_K", "3"))

DATA_DIR = PROJECT_ROOT / "app" / "data"
HISTORY_DIR = DATA_DIR / "history"
CACHE_DIR = DATA_DIR / ".cache"
CHUNKS_PATH = CACHE_DIR / "chunks.json"
EMBEDDINGS_PATH = CACHE_DIR / "embeddings.npy"

OPENROUTER_APP_NAME = os.getenv("OPENROUTER_APP_NAME", "oc-ai-tutor-python")
OPENROUTER_APP_URL = os.getenv("OPENROUTER_APP_URL", "https://example.com")
