"""検索のみを実行して、どのチャンクが選ばれるかを確認する診断ツール。

使い方(コンテナ内):
    python -m app.rag._debug_retrieval "戦国時代を終わらせた戦いは何?"
    python -m app.rag._debug_retrieval "本能寺の変を起こした人物は?" --top-k 5
"""
import argparse

from app.rag.retriever import search


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("query", help="検索したい質問文")
    parser.add_argument("--top-k", type=int, default=5, help="表示する上位件数 (default: 5)")
    args = parser.parse_args()

    chunks = search(args.query, top_k=args.top_k)
    print(f"\nQ: {args.query}")
    print("-" * 60)
    for i, c in enumerate(chunks, start=1):
        preview = c.text.replace("\n", " ")[:80]
        print(f"[{i}] score={c.score:.4f}  {c.source}")
        print(f"    → {preview}...")


if __name__ == "__main__":
    main()
