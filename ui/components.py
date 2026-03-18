import streamlit as st

def render_line(is_yang, is_moving=False):
    color = "#FF4B4B" if is_moving else ("#ffffff" if st.get_option("theme.base") == "dark" else "#000000")
    # For simplicity, we just use inline styles with a fallback generic color for moving lines
    # Using light/dark adaptive CSS might be better, we'll assign classes that adapt nicely.
    
    if is_yang:
        return f"<div style='width: 100%; height: 24px; background-color: {color}; margin-bottom: 6px; border-radius: 2px;'></div>"
    else:
        return f"""
        <div style='display: flex; justify-content: space-between; margin-bottom: 6px;'>
            <div style='width: 44%; height: 24px; background-color: {color}; border-radius: 2px;'></div>
            <div style='width: 44%; height: 24px; background-color: {color}; border-radius: 2px;'></div>
        </div>
        """

def render_hexagram(hexagram_data, lines_binary, moving_indices=None):
    if moving_indices is None:
        moving_indices = []
        
    st.markdown(f"### {hexagram_data['name']}")
    st.markdown(f"**{hexagram_data['trigrams']['upper']}上 {hexagram_data['trigrams']['lower']}下**")
    
    html = "<div style='width: 180px; margin: 10px 0;'>"
    # Render from top to bottom (index 5 down to 0)
    for i in reversed(range(6)):
        is_yang = lines_binary[i] == 1
        is_moving = i in moving_indices
        html += render_line(is_yang, is_moving)
    html += "</div>"
    
    st.markdown(html, unsafe_allow_html=True)
    
    if moving_indices:
        st.markdown("<small style='color:#FF4B4B;'>*紅色代表動爻*</small>", unsafe_allow_html=True)
    
    st.markdown(f"*{hexagram_data['description']}*")
    
    with st.expander("爻辭 (Lines)"):
        # The lines in hexagram_data["lines"] are from bottom to top order.
        for i, line_text in enumerate(hexagram_data["lines"]):
            if i in moving_indices:
                st.markdown(f"**👉 <span style='color:#FF4B4B;'>{line_text}</span>**", unsafe_allow_html=True)
            else:
                st.markdown(line_text)
