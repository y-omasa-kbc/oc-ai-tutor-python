from dataclasses import dataclass

from app.rag.llm import chat
from app.rag.prompts import SYSTEM_PROMPT
from app.rag.query_transformer import transform_query
from app.rag.retriever import RetrievedChunk, search


@dataclass
class RagResult:
    question: str
    transformed_question: str
    answer: str
    sources: list[RetrievedChunk]


def _format_context(chunks: list[RetrievedChunk]) -> str:
    blocks = []
    for i, chunk in enumerate(chunks, start=1):
        blocks.append(f"[資料 {i}] 出典: {chunk.source}\n{chunk.text.strip()}")
    return "\n\n".join(blocks)


def run(query: str, use_query_transformation: bool = True) -> RagResult:
    if not query.strip():
        raise ValueError("質問が空です。")

    search_query = transform_query(query) if use_query_transformation else query
    if not search_query.strip():
        search_query = query

    sources = search(search_query)

    user_prompt = (
        f"質問: {query}\n\n"
        f"参考資料:\n{_format_context(sources)}\n\n"
        "参考資料だけを使って答えてください。"
    )
    answer = chat(
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_prompt},
        ],
    )

    return RagResult(
        question=query,
        transformed_question=search_query,
        answer=answer,
        sources=sources,
    )
