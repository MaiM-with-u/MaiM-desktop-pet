import tomli
from pydantic import BaseModel

class Config(BaseModel):
    url: str = None
    Nickname: str = None
    userNickname: str = None
    platfrom: str = "desktop-pet"
    hide_console: bool = True
    Screenshot_shortcuts: str = None

# 加载 TOML 配置文件
with open("config.toml", "rb") as f:
    config_data = tomli.load(f)

config = Config(**config_data)
