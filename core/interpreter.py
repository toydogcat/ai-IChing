import os
import time
from google import genai
from google.genai import errors
from core.logger import get_logger

logger = get_logger("interpreter")

def get_gemini_client() -> genai.Client | None:
    """取得 Gemini 客戶端"""
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        return None
    return genai.Client(api_key=api_key)

def build_interpretation_prompt(question: str, result: dict, search_context: str = "") -> str:
    """
    根據使用者問題、本卦與變卦，建構 Gemini 提示詞
    """
    has_moving = result["has_moving_lines"]
    orig_hex = result["original_hexagram"]
    changed_hex = result["changed_hexagram"]
    
    prompt = f"使用者問題：{question}\n\n"
    if search_context:
        prompt += f"{search_context}\n\n"
        
    prompt += "卜卦結果：\n"
    prompt += f"本卦：{orig_hex['name']} ({orig_hex['description']})\n"
    
    moving_lines = []
    for i, line in enumerate(result["lines_info"]):
        if line["moving"]:
            moving_lines.append(f"第 {i+1} 爻: {orig_hex['lines'][i]}")
            
    if has_moving:
        prompt += f"動爻：\n" + "\n".join(moving_lines) + "\n"
        prompt += f"變卦：{changed_hex['name']} ({changed_hex['description']})\n"
    else:
        prompt += "無動爻。\n"
        
    prompt += """
## 解讀要求
1. 先簡要概述整體卦象的氛圍
2. 針對問題的具體分析（包含本卦的現況、動爻的轉折事件）
3. 給出針對原本問題的建議與行動指南（變卦的趨勢）
4. 語氣溫暖、專業、有同理心，使用繁體中文
5. 不要使用任何 markdown 格式符號（如 #, *, ** 等），用純文字呈現
6. 段落之間用空行分隔，讓閱讀（與語音轉換）更順暢舒適
"""
    return prompt

def get_ai_interpretation(question: str, result: dict) -> str:
    """
    呼叫 Gemini API 取得 AI 解卦
    """
    client = get_gemini_client()
    if not client:
        return "⚠️ 請先在 .env 中設定 GEMINI_API_KEY 才能使用 AI 解卦功能。"

    MODEL_ID = "gemini-3.1-flash-lite-preview"
    prompt = build_interpretation_prompt(question, result)

    max_retries = 3
    for attempt in range(max_retries):
        try:
            logger.info(f"Calling {MODEL_ID} for interpretation (Attempt {attempt + 1}/{max_retries})...")
            response = client.models.generate_content(
                model=MODEL_ID,
                contents=prompt,
            )
            return response.text
            
        except errors.ClientError as e:
            # 偵測是否為配額已滿 (HTTP 429)
            if e.code == 429:
                wait_time = (attempt + 1) * 10
                logger.warning(f"⚠️ 配額已滿 (429 Error)。將在 {wait_time} 秒後重試...")
                
                if attempt < max_retries - 1:
                    time.sleep(wait_time)
                    continue
                else:
                    logger.error("API quota exceeded after max retries.")
                    return "❌ 目前 API 使用量已達上限，請稍後再試。"
            
            # 其他 Client 錯誤
            logger.error(f"Gemini Client Error: {e}")
            return "error"

        except Exception as e:
            # 系統性錯誤
            logger.error(f"Unexpected error: {e}")
            return "error"

    return "error"
