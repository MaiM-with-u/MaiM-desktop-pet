from pydantic import BaseModel


class Config(BaseModel):
    """Plugin Config Here"""
    url:str="ws://127.0.0.1:8000/ws"  # 你的FastAPI地址 / 与maimcore的服务器（端口）相同
    Nickname :str = "麦麦"              #你的bot昵称
    userNickname :str = ""        #请填入自己的昵称
    platfrom :str = "desktop-pet"    #如果你不知道这是什么那你就不要动它
