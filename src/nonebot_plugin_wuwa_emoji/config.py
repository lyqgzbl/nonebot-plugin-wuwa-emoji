from nonebot import get_plugin_config
from pydantic import BaseModel


class Config(BaseModel):
    wuwa_emoji_token: str | None = None


plugin_config = get_plugin_config(Config)
