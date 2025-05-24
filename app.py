import streamlit as st
from datetime import datetime
from modules.trihex_diagnosis_module import trihex_diagnose

# ページ設定
st.set_page_config(page_title="魂診断 TriHexϕ", page_icon="🍒")

# タイトル表示
st.markdown("<h1 style='text-align: center;'>🍒 魂診断 TriHexϕ</h1>", unsafe_allow_html=True)

# 入力フォーム
name = st.text_input("お名前（ニックネーム）")
birth_date = st.date_input(
    "生年月日（西暦）",
    min_value=datetime(1900, 1, 1),
    max_value=datetime(2040, 12, 31),
    format="YYYY/MM/DD"
)
current_kanji = st.text_input("今のあなたを表す漢字一文字")
ideal_kanji = st.text_input("理想の魂状態を表す漢字一文字")

# 診断ボタン
if st.button("診断する"):
    try:
        result = trihex_diagnose(
            name=name,
            year=birth_date.year,
            month=birth_date.month,
            day=birth_date.day,
            current=current_kanji,
            ideal=ideal_kanji
        )

        st.success("✨ 診断結果 ✨")
        for key, value in result.items():
            st.write(f"**{key}**: {value}")

    except Exception as e:
        st.error(f"診断処理中にエラーが発生しました: {e}")
