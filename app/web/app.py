import os
import sys
from pathlib import Path

import streamlit as st

PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from app.rag.config import OPENROUTER_API_KEY, RETRIEVAL_TOP_K
from app.rag.pipeline import run
from app.rag.prompts import SYSTEM_PROMPT


st.set_page_config(
    page_title="AI 家庭教師 (安土桃山〜江戸初期)",
    page_icon="📜",
    layout="wide",
)


if not OPENROUTER_API_KEY:
    st.error(
        "OPENROUTER_API_KEY が設定されていません。"
        "`.env` を作成し、OpenRouter の API キーを設定してください。"
    )
    st.stop()


@st.cache_data(show_spinner=False)
def _render_sources(sources):
    return [
        {"source": s.source, "text": s.text, "score": round(s.score, 4)} for s in sources
    ]


with st.sidebar:
    st.header("⚙️ 設定")

    use_query_transformation = st.toggle(
        "質問改善 (Query Transformation)",
        value=False,
        help="質問を検索しやすい形に書き換えてから探します。",
    )
    top_k = st.slider("参考資料の数", min_value=1, max_value=5, value=RETRIEVAL_TOP_K)

    st.divider()
    st.subheader("現在のシステムプロンプト")
    st.code(SYSTEM_PROMPT, language="text")
    st.caption("変更するには `app/rag/prompts.py` を編集して保存してください。")

    st.divider()
    st.subheader("📖 実習用テキスト")
    textbook_path = PROJECT_ROOT / "textbook" / "index.html"
    if textbook_path.exists():
        st.markdown(
            f"<a href='{textbook_path.as_uri()}' target='_blank'>"
            "テキストを開く (file://)</a>",
            unsafe_allow_html=True,
        )
    else:
        st.caption("(textbook/ が見つかりません)")


st.title("📜 AI 家庭教師 (安土桃山〜江戸初期)")
st.caption("本能寺の変(1582)から家康の死(1616)まで、資料をもとに答えます。")

question = st.text_input(
    "質問を入力してください",
    placeholder="例: 本能寺の変を起こした人物は?",
    label_visibility="visible",
)
ask = st.button("送信", type="primary", use_container_width=True)

if ask:
    if not question.strip():
        st.warning("質問を入力してください。")
        st.stop()

    with st.spinner("資料を探して、答えを作っています..."):
        try:
            result = run(
                query=question,
                use_query_transformation=use_query_transformation,
            )
        except FileNotFoundError as e:
            st.error(str(e))
            st.stop()
        except Exception as e:
            st.error(f"エラーが発生しました: {e}")
            st.stop()

    st.subheader("💬 回答")
    st.write(result.answer)

    if use_query_transformation and result.transformed_question != result.question:
        with st.expander("🔄 質問改善の結果を見る", expanded=False):
            st.write("**もとの質問:**")
            st.code(result.question, language="text")
            st.write("**書き換えた検索クエリ:**")
            st.code(result.transformed_question, language="text")

    st.subheader("📚 参考にした資料")
    sources = _render_sources(result.sources[:top_k])
    if not sources:
        st.info("該当する資料が見つかりませんでした。")
    for i, s in enumerate(sources, start=1):
        with st.expander(f"[資料 {i}] {s['source']}  (score={s['score']})", expanded=(i == 1)):
            st.write(s["text"])
