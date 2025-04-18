from maim_message import UserInfo,Seg,MessageBase,BaseMessageInfo,FormatInfo

from config import config
import time
from src.core.router import router
from src.util.logger import logger




class chat:
    def __init__(self):
        self.format_info = FormatInfo(
            # 消息内容中包含的Seg的type列表
            content_format=["text", "image", "emoji"],
            # 消息发出后，期望最终的消息中包含的消息类型，可以帮助某些plugin判断是否向消息中添加某些消息类型
            accept_format=["text"],
        )


    async def easy_to_send (self,text : str,type:str):
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
            additional_config={"maimcore_reply_probability_gain": 1},
            format_info=self.format_info,
    )
        message_seg = Seg(
            type = type,
            data = text,  
            )
        
        message_base = MessageBase(message_info,message_seg,raw_message=text)


        # logger.info(payload)
        logger.info("消息发送成功")
        await router.send_message(message_base)


chat_util = chat()