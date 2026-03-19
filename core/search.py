import os
from google import genai
from tavily import TavilyClient
from core.logger import get_logger

logger = get_logger("search")

def summarize_with_gemma(tavily_text: str) -> str:
    """
    將 Tavily 搜尋結果交給 Gemma 進行統整
    """
    if not tavily_text.strip():
        return "沒有提供搜尋結果可以整理。"

    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        logger.warning("未設定 GEMINI_API_KEY，無法呼叫 Gemma，略過整理。")
        return tavily_text

    client = genai.Client(api_key=api_key)
    
    # 使用 Gemma 3 27B 作為內容生成的引擎
    MODEL_ID = "gemma-3-27b-it"
    
    # 建構 Prompt 提示詞
    prompt = f"""
    你是一位專業的內容編輯。請閱讀以下來自外部搜尋引擎的原始資訊，
    並將其整理成一段約 200 字的繁體中文流暢摘要。
    
    要求：
    1. 剔除重複的資訊。
    2. 使用專業、客觀的語氣。
    3. 在摘要結尾，列出 3 個核心關鍵字。
    
    原始資訊：
    {tavily_text}
    """

    try:
        logger.info(f"正在呼叫 {MODEL_ID} 進行摘要整理...")
        response = client.models.generate_content(
            model=MODEL_ID,
            contents=prompt,
        )
        return response.text
    except Exception as e:
        logger.error(f"Gemma 整理失敗: {e}")
        # 如果失敗，回傳原始搜尋結果當作 fallback
        return tavily_text

def perform_tavily_search(query: str, topic="news", search_depth="advanced", max_results=5, days=3) -> tuple[str, bool]:
    """
    執行 Tavily 搜尋並返回摘要字串
    返回：(整理好的摘要字串, bool是否搜尋成功(未發生預期外錯誤))
    """
    api_key = os.getenv("TAVILY_API_KEY")
    if not api_key or api_key == "your_tavily_api_key_here":
        logger.warning("未設定 TAVILY_API_KEY，略過搜尋。")
        return "", False

    try:
        tavily = TavilyClient(api_key=api_key)
        logger.info(f"正在搜尋 Tavily (query: {query})...")
        response = tavily.search(
            query=query,
            topic=topic,
            search_depth=search_depth,
            max_results=max_results,
            days=days
        )
        
        results = response.get("results", [])
        if not results:
            logger.info("Tavily 找不到相關新聞/資料。")
            return "", True

        text_lines = []
        for result in results:
            title = result.get('title', '無標題')
            content = result.get('content', '').replace("\n", " ")
            text_lines.append(f"標題: {title}\n摘要這段: {content}")
        
        raw_results = "\n---\n".join(text_lines)
        
        # 呼叫 Gemma 將原始結果整理成結構化摘要
        summary = summarize_with_gemma(raw_results)
        
        final_context = f"【外部知識庫 / 近期新聞 (Gemma 彙整)】\n{summary}"
        return final_context, True

    except Exception as e:
        logger.error(f"Tavily 搜尋發生錯誤: {e}")
        return "", False
