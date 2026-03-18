import streamlit as st
from core.engine import perform_divination
from dotenv import load_dotenv
import os

load_dotenv()

st.set_page_config(page_title="AI I Ching - 易經自動算命", page_icon="☯️", layout="wide")

def render_hexagram_ui(hexagram_data, binary_lines, moving_indices):
    """
    負責繪製易經六爻。
    hexagram_data: dic，內含卦名、卦辭等資訊
    binary_lines: list，包含 1 (陽) 或 0 (陰)
    moving_indices: list，動爻的索引值 (0~5)
    """
    st.subheader(f"{hexagram_data['name']} ({hexagram_data['trigrams']['upper']}上 {hexagram_data['trigrams']['lower']}下)")
    
    # 易經爻象是由下往上畫（初爻在最底），所以視覺渲染時迴圈要反轉 (reverse)
    for i in reversed(range(6)):
        is_moving = i in moving_indices
        is_yang = bool(binary_lines[i]) 
        
        # 動爻用紅色強調，靜爻用預設文字顏色
        color = "#ef4444" if is_moving else "currentColor"
        
        if is_yang:
            # 陽爻 ───
            html = f'<div style="width: 180px; height: 24px; background-color: {color}; margin: 8px 0; border-radius: 4px;"></div>'
        else:
            # 陰爻 ─ ─
            html = f'''
            <div style="width: 180px; display: flex; justify-content: space-between; margin: 8px 0;">
                <div style="width: 45%; height: 24px; background-color: {color}; border-radius: 4px;"></div>
                <div style="width: 45%; height: 24px; background-color: {color}; border-radius: 4px;"></div>
            </div>
            '''
        # 每一次單獨渲染 HTML，避免合併字串時 Streamlit 框架解析異常
        st.markdown(html, unsafe_allow_html=True)
        
    st.markdown(f"*{hexagram_data['description']}*")
    
    with st.expander("爻辭 (Lines)"):
        # The lines in hexagram_data["lines"] are from bottom to top order.
        for i, line_text in enumerate(hexagram_data["lines"]):
            if i in moving_indices:
                st.markdown(f"**👉 <span style='color:#ef4444;'>{line_text}</span>**", unsafe_allow_html=True)
            else:
                st.markdown(line_text)

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
        render_hexagram_ui(result["original_hexagram"], original_binary, moving_indices)
        
    with col2:
        if result["has_moving_lines"]:
            st.header("變卦 (Changed)")
            changed_binary = [line["changed"] for line in result["lines_info"]]
            render_hexagram_ui(result["changed_hexagram"], changed_binary, [])
        else:
            st.header("變卦 (Changed)")
            st.info("此次占卜無動爻，故無變卦。")
            
st.markdown("---")
st.markdown("💡 *未來擴充：結合 AI 提供白話文解卦建議。*")
