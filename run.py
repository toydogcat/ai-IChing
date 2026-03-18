#!/usr/bin/env python3
"""
啟動腳本：自動結合 Streamlit 與 Ngrok (如果有設定 NGROK_AUTHTOKEN) 進行外網分享
"""
import os
import sys
import time
import subprocess
import logging
from dotenv import load_dotenv

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

def main():
    load_dotenv()
    
    port = os.getenv("STREAMLIT_SERVER_PORT", "8501")
    
    cmd = [
        sys.executable, "-m", "streamlit", "run", "app.py",
        "--server.address=0.0.0.0",
        f"--server.port={port}"
    ]
    
    logging.info("啟動 Streamlit (Local: http://0.0.0.0:%s)", port)
    streamlit_process = subprocess.Popen(cmd)
    
    time.sleep(3) # Wait slightly for streamlit to bind to port
    
    auth_token = os.getenv("NGROK_AUTHTOKEN")
    listener = None
    if auth_token:
        try:
            import ngrok
            logging.info("已設定 NGROK_AUTHTOKEN，啟動 Ngrok 隧道...")
            # ngrok-python package uses ngrok.forward
            listener = ngrok.forward(f"localhost:{port}", authtoken=auth_token)
            logging.info(f"🚀 Ngrok 隧道開啟成功！遠端存取請前往: {listener.url()}")
        except ImportError:
            logging.error("找不到 ngrok 套件，請執行: pip install ngrok")
        except Exception as e:
            logging.error(f"Ngrok 啟動失敗: {e}")
    else:
        logging.info("未設定 NGROK_AUTHTOKEN，僅提供本機服務。")

    try:
        logging.info("伺服器運行中。按 Ctrl+C 停止。")
        streamlit_process.wait()
    except KeyboardInterrupt:
        logging.info("正在關閉伺服器...")
        if listener:
            try:
                import ngrok
                ngrok.disconnect(listener.url())
                logging.info("Ngrok 隧道已關閉。")
            except Exception as e:
                logging.error(f"關閉 Ngrok 時發生錯誤: {e}")
        streamlit_process.terminate()
        streamlit_process.wait()
        logging.info("伺服器已安全停止。")

if __name__ == "__main__":
    main()
