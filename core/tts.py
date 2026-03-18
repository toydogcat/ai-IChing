import os
import asyncio
import urllib.request
from core.logger import get_logger

try:
    import edge_tts
except ImportError:
    edge_tts = None

try:
    import pyttsx3
except ImportError:
    pyttsx3 = None

logger = get_logger("tts")

# Audio is stored inside history/audio/
AUDIO_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "history", "audio")
os.makedirs(AUDIO_DIR, exist_ok=True)

VOICE = "zh-TW-HsiaoChenNeural"

def check_internet():
    try:
        # Check connection using a reliable host
        urllib.request.urlopen("http://8.8.8.8", timeout=2)
        return True
    except:
        return False

async def _generate_audio_async(text, file_path):
    communicate = edge_tts.Communicate(text, VOICE)
    await communicate.save(file_path)

def generate_audio_offline(text, file_path):
    if not pyttsx3:
        logger.error("pyttsx3 is not installed. Offline fallback failed.")
        return None
    try:
        engine = pyttsx3.init()
        # You could optionally map to specific voices for pyttsx3 here in the future
        engine.save_to_file(text, file_path)
        engine.runAndWait()
        logger.info(f"Offline Pyttsx3 Audio generated successfully: {file_path}")
        return file_path
    except Exception as e:
        logger.error(f"Failed to generate Pyttsx3 offline audio: {e}")
        return None

def generate_audio(text, record_id):
    if not text or text.startswith("⚠️") or text == "error":
        return None
        
    # Remove markdown/special chars to protect TTS voice inflection.
    clean_text = text.replace("*", "").replace("#", "")
        
    file_name = f"reading_{record_id}.mp3"
    file_path = os.path.join(AUDIO_DIR, file_name)
    
    if check_internet() and edge_tts is not None:
        try:
            asyncio.run(_generate_audio_async(clean_text, file_path))
            logger.info(f"Edge TTS Audio generated successfully: {file_path}")
            return file_path
        except Exception as e:
            logger.error(f"Edge TTS failed: {e}. Falling back to offline Pyttsx3.")
            return generate_audio_offline(clean_text, file_path)
    else:
        msg = "No internet connection detected" if not check_internet() else "edge_tts package missing"
        logger.info(f"{msg}. Attempting offline Pyttsx3 fallback.")
        return generate_audio_offline(clean_text, file_path)
