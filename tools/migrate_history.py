import os
import json
import argparse
from datetime import datetime
import sys

# 確保可以 import core
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.logger import get_logger
from core.history import get_history_dates, load_history, HISTORY_DIR

logger = get_logger("migrate")

def main():
    dates = get_history_dates()
    total_migrated = 0
    for d in dates:
        file_path = os.path.join(HISTORY_DIR, f"{d}.json")
        records = load_history(d)
        modified = False
        
        for r in records:
            ai_status = r.get("ai_status")
            if not isinstance(ai_status, dict):
                # Migrating from string to dict
                new_status = {
                    "interpretation": ai_status if ai_status in ["success", "recovered", "error"] else "error",
                    "audio": "success" if ai_status in ["success", "recovered"] else "error"
                }
                r["ai_status"] = new_status
                modified = True
                total_migrated += 1
                
        if modified:
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(records, f, ensure_ascii=False, indent=2)
            logger.info(f"✅ Migrated {d}.json")
            
    logger.info(f"🎉 Migration complete. Total records migrated: {total_migrated}")

if __name__ == "__main__":
    main()
