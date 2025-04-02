import sys
import threading
from PyQt5.QtWidgets import QApplication
import uvicorn
from api import fastapi
from pet import chat_pet,app
from util import logger

def run_fastapi():
    uvicorn.run(fastapi, host="0.0.0.0", port=18002)

global_chat_pet = None

if __name__ == "__main__":
    # 启动 FastAPI 线程
    api_thread = threading.Thread(target=run_fastapi, daemon=True)
    api_thread.start()
    logger.info("在拖拽")
    # 启动 Qt
    chat_pet.show()
    sys.exit(app.exec_())