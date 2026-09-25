class WuwaEmojiError(Exception):
    """鸣潮表情包插件基础异常"""


class CharacterNotFoundError(WuwaEmojiError):
    """指定角色不存在或无公开表情"""


class ApiAuthError(WuwaEmojiError):
    """API Token 无效、已停用或已过期"""


class NetworkError(WuwaEmojiError):
    """网络请求或图片下载失败"""
