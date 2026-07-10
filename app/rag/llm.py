import os
from typing import Iterable

import requests

from app.rag.config import (
    OPENROUTER_API_KEY,
    OPENROUTER_APP_NAME,
    OPENROUTER_APP_URL,
    OPENROUTER_MODEL,
)

OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"


def chat(
    messages: Iterable[dict],
    model: str | None = None,
    temperature: float = 0.3,
) -> str:
    api_key = os.getenv("OPENROUTER_API_KEY", OPENROUTER_API_KEY)
    if not api_key:
        raise RuntimeError(
            "OPENROUTER_API_KEY が未設定です。`.env` を確認してください。"
        )

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "HTTP-Referer": OPENROUTER_APP_URL,
        "X-Title": OPENROUTER_APP_NAME,
    }
    payload = {
        "model": model or OPENROUTER_MODEL,
        "messages": list(messages),
        "temperature": temperature,
    }

    response = requests.post(OPENROUTER_URL, headers=headers, json=payload, timeout=60)
    if response.status_code >= 400:
        raise RuntimeError(
            f"OpenRouter API エラー ({response.status_code}): {response.text}"
        )
    data = response.json()
    return data["choices"][0]["message"]["content"].strip()
