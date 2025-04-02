from fastapi import FastAPI, Request
import uvicorn
from util import logger
from pet import chat_pet

fastapi = FastAPI()

@fastapi.post("/api/message")
async def handle_request(request: Request):

    try:
        # 接收并解析JSON数据
        json_data = await request.json()
        # logger.info(f"收到请求数据: {json_data}")

        # message_info = json_data.get('message_info', {})
        message_segment = json_data.get('message_segment', {})
        message_content = message_segment.get('data',{})

        chat_pet.show_message(str(message_content))
        # group_id = message_info.get('group_info', {}).get('group_id')
        # user_id = message_info.get('user_info', {}).get('user_id')


        # 初始化消息链和回复ID
    
    except Exception as e:
        logger.error(f"处理请求时出错: {str(e)}")
        return {"status": "error", "message": str(e)}
