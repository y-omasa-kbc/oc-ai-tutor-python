import json
from pathlib import Path

import numpy as np

from app.rag.config import (
    CACHE_DIR,
    CHUNKS_PATH,
    EMBEDDINGS_PATH,
    HISTORY_DIR,
)
from app.rag.embeddings import embed_texts


def load_markdown_files(directory: Path) -> list[dict]:
    chunks: list[dict] = []
    for path in sorted(directory.glob("*.md")):
        text = path.read_text(encoding="utf-8").strip()
        if not text:
            continue
        chunks.append({"source": path.name, "text": text})
    return chunks


def build_index() -> None:
    if not HISTORY_DIR.exists():
        raise FileNotFoundError(f"ナレッジディレクトリが見つかりません: {HISTORY_DIR}")

    chunks = load_markdown_files(HISTORY_DIR)
    if not chunks:
        raise RuntimeError(f"ナレッジが空です: {HISTORY_DIR}")

    CACHE_DIR.mkdir(parents=True, exist_ok=True)

    with CHUNKS_PATH.open("w", encoding="utf-8") as f:
        json.dump(chunks, f, ensure_ascii=False, indent=2)

    embeddings = np.array(
        embed_texts([chunk["text"] for chunk in chunks]),
        dtype=np.float32,
    )
    np.save(EMBEDDINGS_PATH, embeddings)

    print(f"[index] {len(chunks)} 件のチャンクを {CHUNKS_PATH} に保存しました。")
    print(f"[index] 埋め込み行列 shape={embeddings.shape} を {EMBEDDINGS_PATH} に保存しました。")


if __name__ == "__main__":
    build_index()
