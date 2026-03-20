import streamlit as st
import os
from datetime import datetime
from dotenv import load_dotenv

from core.engine import perform_divination
from core.history import save_reading, update_record_interpretation, search_history_records, get_history_dates, load_history
from core.tts import generate_audio
from core.interpreter import get_ai_interpretation, build_interpretation_prompt
from core.logger import get_logger
from core.search import perform_tavily_search

load_dotenv()
logger = get_logger("app")

st.set_page_config(page_title="AI I Ching - 易經自動算命", page_icon="☯️", layout="wide")

def render_hexagram_ui(hexagram_data, binary_lines, moving_indices):
    """
    負責繪製易經六爻及對應的卦象圖片。
    """
    hex_id = hexagram_data.get('id')
    if hex_id:
        img_format = st.session_state.get("image_format", "jpg")
        img_path = os.path.join("assets", "images", "hexagrams", f"{hex_id}.{img_format}")
        if os.path.exists(img_path):
            st.image(img_path, use_container_width=True)
            
    st.subheader(f"{hexagram_data['name']} ({hexagram_data['trigrams']['upper']}上 {hexagram_data['trigrams']['lower']}下)")
    
    for i in reversed(range(6)):
        is_moving = i in moving_indices
        is_yang = bool(binary_lines[i]) 
        
        color = "#ef4444" if is_moving else "currentColor"
        
        if is_yang:
            html = f'<div style="width: 180px; height: 24px; background-color: {color}; margin: 8px 0; border-radius: 4px;"></div>'
        else:
            html = f'''
            <div style="width: 180px; display: flex; justify-content: space-between; margin: 8px 0;">
                <div style="width: 45%; height: 24px; background-color: {color}; border-radius: 4px;"></div>
                <div style="width: 45%; height: 24px; background-color: {color}; border-radius: 4px;"></div>
            </div>
            '''
        st.markdown(html, unsafe_allow_html=True)
        
    st.markdown(f"*{hexagram_data['description']}*")
    
    with st.expander("爻辭 (Lines)"):
        for i, line_text in enumerate(hexagram_data["lines"]):
            if i in moving_indices:
                st.markdown(f"**👉 <span style='color:#ef4444;'>{line_text}</span>**", unsafe_allow_html=True)
            else:
                st.markdown(line_text)

# === 側邊欄 ===
with st.sidebar:
    st.markdown("# ☯️ AI I Ching")
    st.markdown("---")

    page = st.radio(
        "📄 頁面",
        ["☯️ 卜卦", "📜 歷史紀錄"],
        label_visibility="collapsed",
    )

    st.markdown("---")
    
    if page == "☯️ 卜卦":
        st.markdown("🖼️ **圖片設定**")
        image_format = st.radio(
            "選擇顯示格式",
            options=["jpg", "png"],
            index=0,
            horizontal=True,
            label_visibility="collapsed"
        )
        st.session_state["image_format"] = image_format
        st.markdown("---")
        
        draw_button = st.button("🎲 開始卜卦", type="primary", use_container_width=True)
        st.markdown("---")
        st.markdown(
            "<p style='text-align:center; color:#888; font-size:0.8rem;'>"
            "✨ 靜心冥想你的問題<br>然後點擊卜卦 ✨"
            "</p>",
            unsafe_allow_html=True,
        )

# === 卜卦頁面 ===
if page == "☯️ 卜卦":
    st.title("☯️ AI I Ching (易經自動算命)")
    
    if "user_question_input" not in st.session_state:
        st.session_state["user_question_input"] = ""

    from core.stt import process_transcription
    from streamlit_mic_recorder import mic_recorder

    col1, col2 = st.columns([0.8, 0.2], vertical_alignment="bottom")
    with col2:
        st.markdown("🗣️ **語音輸入**")
        audio_record = mic_recorder(
            start_prompt="錄音 🎤",
            stop_prompt="停止 ⏹️",
            key='recorder'
        )

    if audio_record:
        audio_bytes = audio_record['bytes']
        audio_hash = hash(audio_bytes)
        if st.session_state.get("last_audio_hash") != audio_hash:
            result = process_transcription(audio_bytes, format_hint="webm")
            if result and not result.startswith(("⚠️", "❌")):
                st.session_state["user_question_input"] = result
                st.success("✅ 辨識成功！請在下方確認或修改。")
            else:
                st.error(result)
            st.session_state["last_audio_hash"] = audio_hash

    # 使用者提問輸入框 (若語音辨識成功，會透過 key 自動帶入)
    user_question = st.text_area(
        "🔮 請輸入你想問易經的問題，或用語音輸入直接修改：",
        placeholder="例如：我最近的感情運勢如何？/ 我該不該換工作？/ 這段關係的未來走向是什麼？",
        height=80,
        key="user_question_input"
    )

    if 'draw_button' in locals() and draw_button:
        if not user_question.strip():
            st.warning("請先輸入你想問的問題再卜卦 🙏")
        else:
            logger.info(f"使用者提問：{user_question.strip()}")
            
            search_context = ""
            search_status = "skipped"
            
            with st.spinner("🔍 正在搜尋相關新聞/資料..."):
                search_context, search_success = perform_tavily_search(user_question.strip())
                if search_success:
                    st.toast("✅ 外部資料搜尋成功！", icon="✅")
                    search_status = "success"
                else:
                    st.toast("⚠️ 外部搜尋未設定或無結果，已略過。", icon="⚠️")
                    if os.getenv("TAVILY_API_KEY") and os.getenv("TAVILY_API_KEY") != "your_tavily_api_key_here":
                        search_status = "error"
                    else:
                        search_status = "skipped"

            with st.spinner("神明指引中..."):
                result = perform_divination()
                
            st.session_state["last_result"] = result
            st.session_state["last_question"] = user_question.strip()
            
            logger.info("卜卦完成")
            
            ai_prompt = build_interpretation_prompt(user_question.strip(), result, search_context)
            
            interpretation = None
            with st.spinner("🔮 AI 正在為您解卦..."):
                interpretation = get_ai_interpretation(user_question.strip(), result)
                
            if interpretation and not interpretation.startswith("⚠️") and interpretation != "error":
                logger.info("AI 解卦成功")
            else:
                logger.error(f"AI 解卦失敗: {interpretation}")
                
            st.session_state["last_interpretation"] = interpretation
            
            record_id = save_reading(user_question.strip(), result, interpretation, ai_prompt=ai_prompt, search_status=search_status)
            st.session_state["last_record_id"] = record_id
            
            if interpretation and not interpretation.startswith("⚠️") and interpretation != "error":
                with st.spinner("🎵 正在生成語音..."):
                    audio_path = generate_audio(interpretation, record_id)
                if audio_path:
                    update_record_interpretation(datetime.now().strftime("%Y-%m-%d"), record_id, interpretation, audio_path)
                    st.session_state["last_audio_path"] = audio_path
                else:
                    st.session_state["last_audio_path"] = None

    if "last_result" in st.session_state:
        result = st.session_state["last_result"]
        
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
                
        if "last_interpretation" in st.session_state and st.session_state["last_interpretation"]:
            interpretation = st.session_state["last_interpretation"]
            if interpretation == "error" or interpretation.startswith("⚠️") or interpretation.startswith("❌"):
                st.error("AI 解卦過程中發生錯誤，此次紀錄已標記為 error。")
                if interpretation.startswith("⚠️") or interpretation.startswith("❌"):
                    st.warning(interpretation)
            else:
                st.markdown("---")
                st.header("🔮 AI 深度解讀")
                if st.session_state.get("last_audio_path"):
                    st.audio(st.session_state["last_audio_path"])
                st.markdown(interpretation)
    else:
        st.info("👈 請在左側點擊「開始卜卦」")

# === 歷史紀錄頁面 ===
elif page == "📜 歷史紀錄":
    st.title("📜 卜卦歷史紀錄")
    st.markdown("---")
    
    def render_history_record(record, show_date=False):
        ai_status = record.get("ai_status", {})
        if not isinstance(ai_status, dict):
            ai_status = {
                "interpretation": ai_status if ai_status in ["success", "recovered", "error"] else "error",
                "audio": "success" if ai_status in ["success", "recovered"] else "error",
                "search": "skipped"
            }
            
        interp_status = ai_status.get("interpretation", "error")
        audio_status = ai_status.get("audio", "error")
        search_status = ai_status.get("search", "skipped")
        
        if interp_status == "error":
            status_icon = "❌"
            status_text = "需修復解讀"
        elif audio_status == "error":
            status_icon = "⚠️"
            status_text = "缺少語音需補件"
        else:
            status_icon = "✅"
            status_text = "完成"
            
        date_str = f"[{record.get('_date', '')} " if show_date and "_date" in record else "["
        title_time = f"{date_str}{record['time_display']}] "
        
        title = f"{status_icon} {title_time}{record['question'][:40]}..." if len(record['question']) > 40 else f"{status_icon} {title_time}{record['question']}"
        
        with st.expander(title):
            st.markdown(f"**問題：** {record['question']}")
            st.markdown(f"**ID：** `{record['id']}`")
            st.markdown(f"**AI 狀態：** {status_icon} {status_text} (文字: {interp_status}, 語音: {audio_status}, 搜尋: {search_status})")
            
            orig_hex = record['result']['original_hexagram']
            changed_hex = record['result']['changed_hexagram']
            
            st.markdown("---")
            st.markdown(f"**☯️ 卦象結果：** 本卦：{orig_hex} ｜ 變卦：{changed_hex if changed_hex else '無變卦'}")
            
            for i, line in enumerate(record['result']['lines_info']):
                if line['moving']:
                    st.markdown(f"- 第{i+1}爻：變爻 ({line['value']} {line['symbol']})")
                    
            st.markdown("---")
            if interp_status == "error":
                st.error("AI 解卦失敗。")
            else:
                if record.get("recovered_at"):
                    st.success(f"已於 {record['recovered_at']} 修復")
                if record.get("ai_interpretation_audio_path"):
                    st.audio(record.get("ai_interpretation_audio_path"))
                if record.get("ai_interpretation") and not record.get("ai_interpretation").startswith("⚠️"):
                    st.markdown(f"**AI 解讀：**\n\n{record['ai_interpretation']}")
                else:
                    st.warning(record.get("ai_interpretation"))

    search_query = st.text_input("🔍 搜尋歷史解讀（輸入關鍵字）", "")
    st.markdown("---")
    
    if search_query:
        records = search_history_records(search_query)
        if not records:
            st.info("找不到符合的紀錄。")
        else:
            st.markdown(f"找到 **{len(records)}** 筆相關紀錄：")
            for record in records:
                render_history_record(record, show_date=True)
    else:
        dates = get_history_dates()
        
        if not dates:
            st.info("目前尚無任何卜卦紀錄。")
        else:
            selected_date = st.selectbox("選擇日期", dates)
            records = load_history(selected_date)
            
            if not records:
                st.info(f"{selected_date} 沒有任何紀錄。")
            else:
                st.markdown(f"共 **{len(records)}** 筆紀錄")
                for record in reversed(records):
                    record["_date"] = selected_date
                    render_history_record(record)
