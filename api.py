from fastapi import FastAPI, Request
import uvicorn
from util import logger
from pet import chat_pet
from PyQt5.QtCore import QObject, pyqtSignal, QMetaObject, Q_ARG,Qt
import asyncio
from typing import Optional, Dict, Any

fastapi = FastAPI()

class MessageHandler(QObject):
    """用于处理跨线程消息的QObject"""
    show_message_signal = pyqtSignal(str)

    def __init__(self, pet):
        super().__init__()
        self.pet = pet
        self.show_message_signal.connect(self._handle_show_message)

    def _handle_show_message(self, message):
        """在主线程中安全显示消息"""
        self.pet.show_message(message)

# 创建消息处理器实例
message_handler = MessageHandler(chat_pet)

@fastapi.post("/api/message")
async def handle_request(request: Request):
    try:
        # 接收并解析JSON数据
        json_data = await request.json()
        logger.info(f"收到请求数据: {json_data}")

        # 提取消息内容
        message_segment = json_data.get('message_segment', {})
        message_content = str(message_segment.get('data', ""))

        # 使用信号槽机制安全地跨线程调用UI操作
        QMetaObject.invokeMethod(message_handler, 
                               "show_message_signal", 
                               Qt.QueuedConnection,
                               Q_ARG(str, message_content))

        return {"status": "success", "message": "消息已处理"}
    
    except Exception as e:
        logger.error(f"处理请求时出错: {str(e)}")
        return {"status": "error", "message": str(e)}