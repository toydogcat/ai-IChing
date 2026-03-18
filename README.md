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

## 📂 專案結構

```bash
ai-IChing/
│
├── app.py                     # Streamlit 主程式入口
├── requirements.txt           # 專案套件依賴清單
├── .env.example               # 環境變數範例檔
├── core/
│   └── engine.py              # 核心占卜邏輯與卦象轉換引擎
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

## 🛠 未來規劃
- **AI 深度解卦**：串接大型語言模型 (LLM)，將占卜的變卦與動爻傳遞給 AI，給出客製化的白話文解釋。
- **RAG 歷史哲學知識庫**：導入檢索增強生成 (RAG)，豐富 AI 解答的歷史與典故厚度。
- **互動問答 Agent**：提供 Chatbot 介面，讓使用者能在線上釐清問題並深入對話探討卦意。
