from maim_message import GroupInfo,UserInfo,Seg,MessageBase,BaseMessageInfo
import logging
import httpx
from config import Config
import time
from router import router

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


        # logger.info(payload)
        logger.info("消息发送成功")
        await router.send_message(message_base)


chat_util = chat()