from nonebot import require
from nonebot.log import logger
from nonebot.plugin import PluginMetadata, inherit_supported_adapters

require("nonebot_plugin_alconna")
from nonebot_plugin_alconna import (
    Alconna,
    Args,
    CommandMeta,
    Match,
    UniMessage,
    on_alconna,
)

from .config import Config, plugin_config
from .exceptions import ApiAuthError, CharacterNotFoundError, WuwaEmojiError
from .utils import download_random_emoji

__plugin_meta__ = PluginMetadata(
    name="鸣潮表情包插件",
    description="鸣潮表情包插件",
    usage="/鸣潮表情包 [角色名]",
    type="application",
    homepage="https://github.com/lyqgzbl/nonebot-plugin-wuwa-emoji",
    config=Config,
    supported_adapters=inherit_supported_adapters("nonebot_plugin_alconna"),
    extra={
        "author": "lyqgzbl <admin@lyqgzbl.com>",
        "version": "0.1.0",
    },
)


wuwa_emoji_command = on_alconna(
    Alconna(
        ["鸣潮表情包"],
        Args["character?#指定角色表情包", str],
        meta=CommandMeta(
            compact=True,
            description="鸣潮表情包插件",
            usage=__plugin_meta__.usage,
            example="/鸣潮表情包\n/鸣潮表情包 秧秧",
        ),
    ),
    priority=10,
    block=True,
    use_cmd_start=True,
)


@wuwa_emoji_command.handle()
async def _(character: Match[str]):
    char_name = character.result if character.available else None
    if not plugin_config.wuwa_emoji_token:
        await wuwa_emoji_command.finish(
            "缺失必要配置项 'wuwa_emoji_token', 请在配置文件中添加后重启机器人"
        )
    try:
        emoji_bytes = await download_random_emoji(
            character=char_name, token=plugin_config.wuwa_emoji_token
        )
    except CharacterNotFoundError:
        await wuwa_emoji_command.finish(f"未找到角色「{char_name}」的表情包")
    except ApiAuthError:
        await wuwa_emoji_command.finish(
            "API Token 无效或已过期, 请检查配置项 'wuwa_emoji_token'"
        )
    except WuwaEmojiError as e:
        logger.error(f"获取鸣潮表情包失败: {e}")
        await wuwa_emoji_command.finish("获取表情包失败, 请稍后再试")
    except Exception as e:
        logger.opt(exception=e).error("获取鸣潮表情包时发生未知异常")
        await wuwa_emoji_command.finish("获取表情包时发生未知错误, 请稍后再试")

    await UniMessage.image(raw=emoji_bytes).finish()
