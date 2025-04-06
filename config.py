from pydantic import BaseModel


class Config(BaseModel):
    """Plugin Config Here"""

    Fastapi_url: str = "http://localhost:8000/api/message"  # 你的FastAPI地址 / 与maimcore的服务器（端口）相同
    Nickname: str = "麦麦"  # 你的bot昵称
    userNickname: str = "Maple"
    platfrom: str = "desktop-pet"  # 如果你不知道这是什么那你就不要动它
    allow_group_list: list[str] = []  # 留空则为不启动QQ端白名单
