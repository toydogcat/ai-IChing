import streamlit as st
from core.engine import perform_divination
from ui.components import render_hexagram
from dotenv import load_dotenv
import os

load_dotenv()

st.set_page_config(page_title="AI I Ching - 易經自動算命", page_icon="☯️", layout="wide")

st.title("☯️ AI I Ching (易經自動算命)")

st.markdown("""
點擊下方按鈕進行金錢卦占卜。系統將為您模擬擲出 6 次 3 枚硬幣，產生本卦與變卦，並標示動爻位置。
""")

if st.button("開始卜卦 (Divination)", type="primary"):
    with st.spinner("神明指引中..."):
        result = perform_divination()
        
    st.success("卜卦完成！")
    
    st.markdown("### 🎲 擲幣結果")
    toss_str = " | ".join([f"第{i+1}爻: {t} ({l['symbol']})" for i, (t, l) in enumerate(zip(result['tosses'], result['lines_info']))])
    st.info(toss_str)
    
    col1, col2 = st.columns(2)
    
    original_binary = [line["original"] for line in result["lines_info"]]
    moving_indices = [i for i, line in enumerate(result["lines_info"]) if line["moving"]]
    
    with col1:
        st.header("本卦 (Original)")
        render_hexagram(result["original_hexagram"], original_binary, moving_indices)
        
    with col2:
        if result["has_moving_lines"]:
            st.header("變卦 (Changed)")
            changed_binary = [line["changed"] for line in result["lines_info"]]
            render_hexagram(result["changed_hexagram"], changed_binary, [])
        else:
            st.header("變卦 (Changed)")
            st.info("此次占卜無動爻，故無變卦。")
            
st.markdown("---")
st.markdown("💡 *未來擴充：結合 AI 提供白話文解卦建議。*")
