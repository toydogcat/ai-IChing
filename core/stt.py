import streamlit as st
import speech_recognition as sr
import io
from pydub import AudioSegment

def convert_to_wav(audio_bytes, format_hint=None):
    """將瀏覽器或上傳的音訊轉換為 SpeechRecognition 支援的 WAV 格式"""
    try:
        audio_io = io.BytesIO(audio_bytes)
        
        if format_hint:
            audio = AudioSegment.from_file(audio_io, format=format_hint)
        else:
            audio = AudioSegment.from_file(audio_io)
            
        wav_io = io.BytesIO()
        audio.export(wav_io, format="wav")
        wav_io.seek(0)
        return wav_io
    except Exception as e:
        st.error(f"音訊格式轉換失敗，請確認是否已安裝 ffmpeg。詳細錯誤: {e}")
        return None

def process_transcription(audio_bytes, format_hint=None):
    """執行音訊轉換與語音辨識"""
    with st.spinner("系統正在轉換格式並辨識中..."):
        wav_io = convert_to_wav(audio_bytes, format_hint)
        if not wav_io:
            return None

        r = sr.Recognizer()
        try:
            with sr.AudioFile(wav_io) as source:
                audio_data = r.record(source)
                text = r.recognize_google(audio_data, language="zh-TW")
                return text
                
        except sr.UnknownValueError:
            return "⚠️ 無法辨識語音內容（可能沒說話、聲音太小或雜音過大）。"
        except sr.RequestError as e:
            return f"❌ 無法連線至語音辨識服務: {e}"
        except Exception as e:
            return f"❌ 發生未知的錯誤: {e}"
