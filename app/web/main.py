import sys
from pathlib import Path

import streamlit as st

PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from app.rag.config import OPENROUTER_API_KEY, RETRIEVAL_TOP_K
from app.rag.pipeline import run


st.set_page_config(
    page_title="AI 家庭教師",
    page_icon="📜",
    layout="wide",
)

st.markdown(
    """
    <style>
    header[data-testid="stHeader"] { display: none; }
    [data-testid="stToolbar"] { display: none; }
    [data-testid="stMainBlockContainer"],
    .block-container {
        padding-top: 1rem !important;
    }
    .stApp, .stMarkdown, .stTextInput, .stButton, p, div {
        font-size: 1rem !important;
    }
    h2 { font-size: 0.95rem !important; font-weight: 600 !important; }
    h3 { font-size: 0.9rem !important; }
    code, pre { font-size: 0.85rem !important; }
    </style>
    """,
    unsafe_allow_html=True,
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


TEXTBOOK_URL = "http://localhost:8502/"

st.title("📜 AI 家庭教師")

st.markdown(
    f'<a href="{TEXTBOOK_URL}" target="_blank" '
    f'style="font-size: 0.85em; color: #555; text-decoration: none;">'
    f'📖 実習用テキストを開く</a>',
    unsafe_allow_html=True,
)

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
            result = run(query=question)
        except FileNotFoundError as e:
            st.error(str(e))
            st.stop()
        except Exception as e:
            st.error(f"エラーが発生しました: {e}")
            st.stop()

    st.subheader("💬 回答")
    st.write(result.answer)

    if result.transformed_question != result.question:
        with st.expander("🔄 質問改善の結果を見る", expanded=False):
            st.write("**もとの質問:**")
            st.code(result.question, language="text")
            st.write("**書き換えた検索クエリ:**")
            st.code(result.transformed_question, language="text")

    st.subheader("📚 参考にした資料")
    sources = _render_sources(result.sources[:RETRIEVAL_TOP_K])
    if not sources:
        st.info("該当する資料が見つかりませんでした。")
    for i, s in enumerate(sources, start=1):
        with st.expander(f"[資料 {i}] {s['source']}  (score={s['score']})", expanded=False):
            st.write(s["text"])
