# AI I Ching (易經自動算命)

![Build Status](https://img.shields.io/badge/build-passing-brightgreen)
![Python](https://img.shields.io/badge/python-3.8%2B-blue)
![Streamlit](https://img.shields.io/badge/streamlit-app-red)

這是一個基於 Streamlit 開發的「易經金錢卦自動算命」前端應用程式。系統透過程式模擬傳統的銅錢占卜（擲幣三次決定一爻，共擲六次），自動計算本卦、變卦以及動爻，並結合視覺化呈現，讓使用者輕鬆體驗易經卜卦的樂趣。

## 🎯 核心功能

- **金錢卦模擬 (Coin Toss Simulation)**：自動化拋擲 3 枚硬幣 6 次，準確計算出 6, 7, 8, 9 四種陰陽狀態。
- **動爻判定與變卦**：根據老陰（6）或老陽（9）產生「動爻」，並自動推展出對應的「變卦」。
- **卦象視覺化 (Visual Hexagrams)**：透過自定義的 UI 元件，清晰展示出陰陽爻圖（包含紅色的動爻顏色提示）。
  - **爻辭與卦辭顯示**：內建完整的易經 64 卦資料庫，完整顯示卜出的卦辭與對應爻辭。
- **語音輸入 (Voice Input)**：支援使用麥克風語音輸入占卜問題，自動即時辨識為文字。
- **AI 深度解卦 (AI Interpretation)**：結合 Gemini 語言模型，根據問題、本卦、變卦與動爻，提供專屬的白話文命理解析。
- **外部知識搜尋 (Web Search)**：整合 Tavily 搜尋能力，在 AI 解卦前自動檢索最新網路資訊與背景資料作為輔助參考。
- **語音朗讀合成 (Text-to-Speech)**：AI 解讀結果將自動透過 Edge TTS 轉換為語音，支援流暢發音，並具有離線備援機制保障運作。
- **卜卦歷史紀錄 (History & Recovery)**：自動儲存每一次占卜結果，並提供專屬智能修復機制補齊因網路或 API 問題遺漏的 AI 內容。

## 📂 專案結構

```bash
ai-IChing/
│
├── app.py                     # Streamlit 主程式入口
├── requirements.txt           # 專案套件依賴清單
├── .env.example               # 環境變數範例檔
├── core/
│   ├── engine.py              # 核心占卜邏輯與卦象轉換引擎
│   ├── interpreter.py         # AI 提示詞建構與結果生成
│   ├── logger.py              # 日誌記錄系統
│   ├── search.py              # Tavily 外部搜尋整合
│   ├── stt.py                 # 語音轉文字 (Speech-to-Text) 處理
│   ├── tts.py                 # 文字轉語音 (Text-to-Speech) 引擎
│   └── history.py             # 歷史紀錄管理模組
├── ui/
│   └── components.py          # 負責在網頁上繪製卦象圖的 Streamlit UI 元件
└── data/
    └── hexagrams/
        └── 64_hexagrams.json  # 易經 64 卦繁體中文資料庫
```

## 🚀 快速開始

### 1. 環境設定
建議使用 Conda 或 venv 建立獨立的 Python 環境。
```bash
# 激活你的環境 (例如 Conda 環境)
conda activate toby
```

### 2. 安裝套件
使用 pip 安裝 `requirements.txt` 列出的依賴：
```bash
pip install -r requirements.txt
```

### 3. 環境變數設定檔
複製 `.env.example` 為 `.env` ，目前此專案會透過 python-dotenv 讀取環境變數。
*(未來如果要串接 AI 進行解卦，可將 API Keys 放進這個文件)*
```bash
cp .env.example .env
```

### 4. 啟動應用程式
透過 `run.py` 啟動應用程式。這會一併啟動 Streamlit 與 Ngrok 隧道（如果 `.env` 中有設定 `NGROK_AUTHTOKEN`）：
```bash
python run.py
```
執行後，終端機將顯示本機存取網址，以及 Ngrok 分享的遠端網址。

## 🧰 實用工具 (Utilities)

專案提供了一些輔助開發的腳本工具，放置於 `tools/` 目錄下：

### 圖片批次轉換工具 (PNG to JPG)
這可以用來批次將 `assets/images/` 目錄下的所有 PNG 圖片轉換為 JPG 格式，以節省儲存空間（AI 生成的意境圖常有轉檔需求）。工具會自動處理透明背景並跳過已轉換的檔案。

**基本用法：**
```bash
python tools/convert_png_to_jpg.py
```

**進階用法：**
- **自訂品質** (例如設定為 `90`，預設為 `85`)：
  ```bash
  python tools/convert_png_to_jpg.py 90
  ```
- **轉換後自動刪除**原始 PNG 檔案：
  ```bash
  python tools/convert_png_to_jpg.py --delete
  ```
- **合併使用**：
  ```bash
  python tools/convert_png_to_jpg.py 90 --delete
  ```

## 🛠 未來規劃
- **專業 RAG 歷史哲學知識庫**：在目前的 Tavily 外部搜尋基礎上，進一步建立純粹的易經歷史、易理與典籍專屬向量資料庫。
- **互動問答 Agent**：提供 Chatbot 介面，讓使用者能在線上釐清問題並深入對話探討卦意。
