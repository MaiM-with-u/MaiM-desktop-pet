import tomli
import uuid
from pydantic import BaseModel

class Config(BaseModel):
    url: str = None
    Nickname: str = None
    userNickname: str = None
    platform: str = "desktop-pet"
    hide_console: bool = True
    Screenshot_shortcuts: str = None
    allow_multiple_source_conversion:bool = False #多桌宠连接适配，默认为关



# 加载 TOML 配置文件
with open("config.toml", "rb") as f:
    config_data = tomli.load(f)

config = Config(**config_data)

if config.allow_multiple_source_conversion :
    config.platform = config.platform + str(uuid.uuid4())