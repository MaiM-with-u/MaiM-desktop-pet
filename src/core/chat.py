from maim_message import UserInfo, Seg, MessageBase, BaseMessageInfo, FormatInfo, Router, RouteConfig, TargetConfig

from config import config
import time
import uuid
from src.core.router import router
from src.util.logger import logger




class chat:
    def __init__(self):
        self.format_info = FormatInfo(
            # 消息内容中包含的Seg的type列表
            content_format=["text", "image", "emoji"],
            # 消息发出后，期望最终的消息中包含的消息类型
            accept_format=["text", "image", "emoji"],
        )


    async def easy_to_send (self,text : str,type:str):
        user_info = UserInfo(
            platform = config.platform,
            user_id="0",  # 使用字符串类型的ID
            user_nickname = config.userNickname,
            user_cardname = config.userNickname,
        )

        message_info = BaseMessageInfo(
            platform = config.platform,
            message_id = str(uuid.uuid4()),  # 生成唯一的消息ID
            time = time.time(),  # 使用浮点数时间戳
            group_info= None,
            user_info = user_info,
            format_info=self.format_info,
            additional_config={"maimcore_reply_probability_gain": 1},
        )
        message_seg = Seg(
            type = type,
            data = text,  
            )
        
        message_base = MessageBase(
            message_info=message_info,
            message_segment=message_seg,  # 注意这里使用 message_segment 而不是 message_seg
            raw_message=text
        )


        # logger.info(payload)
        logger.info("消息发送成功")
        await router.send_message(message_base)


chat_util = chat()