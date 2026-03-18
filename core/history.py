import json
import os
from datetime import datetime
import uuid
from core.logger import get_logger

logger = get_logger("history")

HISTORY_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "history")
os.makedirs(HISTORY_DIR, exist_ok=True)

def get_history_file_path(date_str=None):
    if date_str is None:
        date_str = datetime.now().strftime("%Y-%m-%d")
    return os.path.join(HISTORY_DIR, f"{date_str}.json")

def load_history(date_str=None):
    file_path = get_history_file_path(date_str)
    if not os.path.exists(file_path):
        return []
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        logger.error(f"Failed to load history file {file_path}: {e}")
        return []

def save_reading(question, result, interpretation, ai_prompt=""):
    date_str = datetime.now().strftime("%Y-%m-%d")
    time_str = datetime.now().strftime("%H:%M:%S")
    record_id = str(uuid.uuid4())[:8]
    
    file_path = get_history_file_path(date_str)
    history = load_history(date_str)
    
    record = {
        "id": record_id,
        "date": date_str,
        "time_display": time_str,
        "question": question,
        "ai_prompt": ai_prompt,
        "ai_interpretation": interpretation,
        "ai_status": "success" if interpretation and not interpretation.startswith("⚠️") and interpretation != "error" else "error",
        "result": {
            "tosses": result["tosses"],
            "original_hexagram": result["original_hexagram"]["name"] if result["original_hexagram"] else None,
            "changed_hexagram": result["changed_hexagram"]["name"] if result["changed_hexagram"] else None,
            "has_moving_lines": result["has_moving_lines"],
            "lines_info": [{"moving": l["moving"], "symbol": l["symbol"], "value": l["value"]} for l in result["lines_info"]]
        }
    }
    
    history.append(record)
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(history, f, ensure_ascii=False, indent=2)
        
    return record_id

def get_history_dates():
    if not os.path.exists(HISTORY_DIR):
        return []
    files = [f for f in os.listdir(HISTORY_DIR) if f.endswith(".json")]
    dates = [f.replace(".json", "") for f in files]
    dates.sort(reverse=True)
    return dates

def search_history_records(query):
    query = query.lower()
    results = []
    for date_str in get_history_dates():
        records = load_history(date_str)
        for record in records:
            if query in record.get("question", "").lower() or query in record.get("ai_interpretation", "").lower():
                record["_date"] = date_str
                results.append(record)
    return results

def update_record_interpretation(date_str, record_id, interpretation, audio_path=None):
    file_path = get_history_file_path(date_str)
    history = load_history(date_str)
    
    for record in history:
        if record["id"] == record_id:
            record["ai_interpretation"] = interpretation
            record["ai_status"] = "success" if interpretation and not interpretation.startswith("⚠️") and interpretation != "error" else "error"
            if audio_path:
                record["ai_interpretation_audio_path"] = audio_path
            record["recovered_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            break
            
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(history, f, ensure_ascii=False, indent=2)
