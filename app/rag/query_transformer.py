import os

from app.rag.llm import chat

QUERY_REWRITE_SYSTEM_PROMPT = (
    "あなたは日本語の検索クエリを、検索エンジンやベクトル検索にかけやすい形に整えるアシスタントです。"
    "ユーザーの質問が曖昧だったり長かったりする場合は、"
    "元の意図を保ったまま、具体的で簡潔な検索クエリに書き直してください。"
    "質問がすでに明確で短い場合は、そのまま返してください。"
    "余計な説明はせず、書き換えたクエリだけを出力してください。"
)


def transform_query(query: str) -> str:
    return query
