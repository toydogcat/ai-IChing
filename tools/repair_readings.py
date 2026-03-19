import sys
import os
import argparse
import json
from datetime import datetime

# 確保可以 import core
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.logger import get_logger
from core.history import get_history_dates, load_history
from core.tts import generate_audio
from core.interpreter import get_gemini_client

logger = get_logger("repair")

def _save_history(date_str, history):
    from core.history import HISTORY_DIR
    file_path = os.path.join(HISTORY_DIR, f"{date_str}.json")
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(history, f, ensure_ascii=False, indent=2)

def list_errors():
    dates = get_history_dates()
    error_count = 0
    for d in dates:
        records = load_history(d)
        for r in records:
            ai_status = r.get("ai_status", {})
            if not isinstance(ai_status, dict):
                ai_status = {"interpretation": ai_status, "audio": "success" if ai_status in ["success", "recovered"] else "error"}
                
            if ai_status.get("interpretation") == "error" or ai_status.get("audio") == "error":
                print(f"[ERROR/WARNING] Date: {d} | ID: {r['id']} | Q: {r['question']} | Status: {ai_status}")
                error_count += 1
    if error_count == 0:
        print("🎉 恭喜！沒有任何狀態為 error 的紀錄。")
    else:
        print(f"\n總共找到 {error_count} 筆 error 紀錄。")

def repair_record(date_str, record_id=None, repair_all=False):
    client = get_gemini_client()
    if not client:
        logger.error("❌ 找不到 GEMINI_API_KEY，請確認 .env 檔案設定。也可考慮手動從 ai_prompt 複製內容。")
        return

    records = load_history(date_str)
    if not records:
        logger.warning(f"⚠️ 找不到日期 {date_str} 的檔案。")
        return

    modified = False
    repaired_count = 0

    for r in records:
        ai_status = r.get("ai_status", {})
        if not isinstance(ai_status, dict):
            ai_status = {"interpretation": ai_status, "audio": "success" if ai_status in ["success", "recovered"] else "error"}
            
        interp_status = ai_status.get("interpretation", "error")
        audio_status = ai_status.get("audio", "error")
        
        if interp_status != "error" and audio_status != "error":
            continue
            
        if not repair_all and r["id"] != record_id:
            continue

        prompt = r.get("ai_prompt")
        if not prompt and interp_status == "error":
            logger.error(f"❌ ID {r['id']} 缺少 ai_prompt，無法自動修復文字解讀。")
            continue

        try:
            if interp_status == "error":
                logger.info(f"🔄 正在重新呼叫 Gemini 修復 ID: {r['id']} ...")
                # Wait for rate limit mitigation just in case there are many in a row
                import time
                time.sleep(1)
                
                response = client.models.generate_content(
                    model="gemini-3.1-flash-lite-preview",
                    contents=prompt,
                )
                interpretation = response.text
                r["ai_interpretation"] = interpretation
            else:
                logger.info(f"🔄 正在為 ID: {r['id']} 補成語音...")
                interpretation = r.get("ai_interpretation", "")
            
            audio_path = generate_audio(interpretation, r["id"])
            
            if not isinstance(r.get("ai_status"), dict):
                r["ai_status"] = {"interpretation": "recovered", "audio": "recovered"}
                
            r["ai_status"]["interpretation"] = "recovered"
            
            if audio_path:
                r["ai_interpretation_audio_path"] = audio_path
                r["ai_status"]["audio"] = "recovered"
            else:
                r["ai_status"]["audio"] = "error"
                
            r["recovered_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            logger.info(f"✅ 修復完成！ID: {r['id']}")
            modified = True
            repaired_count += 1

        except Exception as e:
            logger.error(f"❌ 發生錯誤, ID {r['id']}: {e}")

        if not repair_all:
            break

    if modified:
        _save_history(date_str, records)
        logger.info(f"💾 存檔完成，共修復 {repaired_count} 筆紀錄。")
    else:
        logger.info("ℹ️ 沒有需要修復或符合條件的紀錄。")

def main():
    parser = argparse.ArgumentParser(description="AI I Ching 歷史紀錄修復腳本")
    parser.add_argument("--list", action="store_true", help="列出所有 error 的紀錄")
    parser.add_argument("--date", type=str, help="指定日期 (YYYY-MM-DD)")
    parser.add_argument("--id", type=str, help="指定要修復的紀錄 ID")
    parser.add_argument("--all", action="store_true", help="修復全部 error 紀錄")
    
    args = parser.parse_args()
    
    if args.list:
        list_errors()
    elif args.date and args.id:
        repair_record(args.date, record_id=args.id)
    elif args.date and args.all:
        repair_record(args.date, repair_all=True)
    elif args.all and not args.date:
        dates = get_history_dates()
        for d in dates:
            repair_record(d, repair_all=True)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
