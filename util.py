from maim_message import GroupInfo,UserInfo,Seg,MessageBase,BaseMessageInfo
import logging
import httpx
from config import Config
import time

logging.basicConfig(
    level=logging.DEBUG,  # 设置日志级别
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler()]  # 输出到控制台
)
# 创建logger
logger = logging.getLogger('pet')
logger.setLevel(logging.DEBUG)  # 设置日志级别
client = httpx.AsyncClient(timeout=60)  # 创建异步HTTP客户端
config = Config()

class chat:
    def __init__(self) -> None:
        self.client = httpx.AsyncClient(timeout=60)  # 创建异步HTTP客户端

    async def easy_to_send (self,text : str):
        user_info = UserInfo(
            platform = config.platfrom,
            user_id=0,#反正得有
            user_nickname = config.userNickname,
            user_cardname = config.userNickname,
        )

        message_info = BaseMessageInfo(
            platform = config.platfrom,
            message_id = None,
            time = int(time.time()),
            group_info= None,
            user_info = user_info,
            additional_config={"maimcore_reply_probability_gain": 1}
    )
        message_seg = Seg(
            type = 'text',
            data = text,  
            )
        
        message_base = MessageBase(message_info,message_seg,raw_message=text)

        payload = message_base.to_dict()
        # logger.info(payload)
        logger.info("消息发送成功")

        response = await self.client.post(
            config.Fastapi_url,
            json=payload,
            headers={"Content-Type": "application/json"}
        )
        
        # 检查响应状态
        if response.status_code != 200:
            logger.error(f"FastAPI返回错误状态码: {response.status_code}")
            logger.debug(f"响应内容: {response.text}")
        else:
            response_data = response.json()
            logger.info(f"收到服务端响应: {response_data}")
            logger.debug(f"响应内容: {response_data}")

chat_util = chat()