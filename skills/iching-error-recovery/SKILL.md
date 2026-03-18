---
name: iching-error-recovery
description: 修復占卜歷史中 AI 解卦失敗 (error) 的紀錄，使用 AI 重新生成解讀與語音
---

# ☯️ I Ching Error Recovery — AI 解卦救援技能

## 功能說明

修復 `history/` 資料夾中 `ai_status` 為 `"error"` 的占卜紀錄。根據該次紀錄中的使用者提問、本卦與變卦抽牌結果，重新呼叫 Gemini API 生成解讀，並補足缺失的 AI 語音。

## 使用時機

- 使用者回報 AI 解卦失敗
- 在 Streamlit 歷史紀錄頁面看到 ❌ 標記的紀錄
- 批次修復所有 error 紀錄

## SOP 操作步驟

### 步驟 1：確認環境

檢查 `.env` 檔中是否有有效的 `GEMINI_API_KEY`，並確認 Python 環境 `PYTHON_PATH`，`CONDA_ENV`。

```bash
cat .env | grep GEMINI_API_KEY
cat .env | grep PYTHON_PATH
cat .env | grep CONDA_ENV
```

### 步驟 2：查看 error 紀錄

使用修復腳本查看所有 error 紀錄：

```bash
conda activate toby
python tools/repair_readings.py --list
```

這會列出所有 AI 狀態為 error 的紀錄，包含日期、ID、問題和卦象。

### 步驟 3：修復紀錄

若有有效的 `GEMINI_API_KEY`，則執行以下指令自動修復：

修復單筆紀錄：
```bash
python tools/repair_readings.py --date 2026-03-17 --id abc12345
```

修復某天所有 error 紀錄：
```bash
python tools/repair_readings.py --date 2026-03-17 --all
```

修復所有日期的所有 error 紀錄：
```bash
python tools/repair_readings.py --all
```

> **手動模式 (無 API Key)**：若無有效的 API Key，助手應指示使用者或自行讀取 error 紀錄中的 `ai_prompt` 欄位值，提交給 Gemini 網頁版產生回覆後，再手動把文字與狀態更正回 JSON 紀錄。

### 步驟 4：生成語音與 fallback 機制

腳本或應用程式在成功取回解答後，會自動產生語音並更新紀錄中的 `ai_interpretation_audio_path`：
- **有網路連線時**：優先使用 Edge TTS (台灣口音女聲 `zh-TW-HsiaoChenNeural`) 產生高品質的 `.mp3` 語音。
- **無網路連線或是連線異常時**：系統將自動 fallback 到離線的 `pyttsx3` 套件進行語音生成發音，確保專案無論是否連網皆可順暢運作不中斷。

### 步驟 5：驗證修復結果

修復後，不論採用自動或手動，只要有正確的解卦內容，紀錄的 `ai_status` 就會被改為 `"recovered"` 並加入 `recovered_at`。
可在 Streamlit 歷史紀錄子頁面中確認：
- ✅ = 原始成功
- 🔄 = 已修復
- ❌ = 尚未修復

## 相關檔案

| 檔案 | 用途 |
|------|------|
| `tools/repair_readings.py` | 專屬的修復與語音生成腳本 |
| `core/history.py` | History 紀錄管理模組 |
| `core/tts.py` | TTS 語音生成本體（包含連線與斷線 fallback 切換邏輯）|
| `core/interpreter.py` | Gemini 提示詞與金錢卦解析建構 |
| `history/*.json` | 占卜紀錄檔案（主要修復目標） |
