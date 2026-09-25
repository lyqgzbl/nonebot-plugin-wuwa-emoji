import httpx
from nonebot import get_driver
from nonebot.log import logger

from .exceptions import ApiAuthError, CharacterNotFoundError, NetworkError

WUWA_RANDOM_EMOJI_API = (
    "https://emoji.wuwa.games/apis/api.random-emoji.wuwa.games/v1alpha1/random"
)

_httpx_client: httpx.AsyncClient | None = None


def get_httpx_client() -> httpx.AsyncClient:
    global _httpx_client
    if _httpx_client is None:
        _httpx_client = httpx.AsyncClient(
            timeout=20.0,
            follow_redirects=True,
            limits=httpx.Limits(
                max_connections=20,
                max_keepalive_connections=10,
            ),
        )
    return _httpx_client


driver = get_driver()


@driver.on_shutdown
async def _():
    if _httpx_client:
        await _httpx_client.aclose()


async def download_random_emoji(
    token: str,
    character: str | None = None,
) -> bytes:
    """异步获取并下载鸣潮随机表情包

    :param character: 可选角色名称 (如 "爱弥斯")
    :param token: API Token
    :return: 表情包二进制数据
    :raises CharacterNotFoundError: 角色不存在或没有公开表情
    :raises ApiAuthError: API Token 无效、已停用或已过期
    :raises NetworkError: 网络请求或下载失败
    """
    client = get_httpx_client()

    headers: dict[str, str] = {}
    if token:
        headers["Authorization"] = f"Bearer {token}"

    params: dict[str, str] = {}
    if character:
        params["character"] = character.strip()

    try:
        resp = await client.get(
            WUWA_RANDOM_EMOJI_API,
            params=params,
            headers=headers,
        )
    except httpx.RequestError as e:
        logger.error(f"请求鸣潮表情包 API 失败: {e}")
        raise NetworkError(f"请求表情包接口异常: {e}") from e

    if resp.status_code == 404:
        raise CharacterNotFoundError(f"未找到角色「{character}」的公开表情包")
    if resp.status_code in (401, 403):
        raise ApiAuthError("API Token 无效、已停用或已过期")
    if resp.is_error:
        logger.error(f"表情包 API 响应错误: {resp.status_code} - {resp.text}")
        raise NetworkError(f"表情包 API 返回错误状态码: {resp.status_code}")

    try:
        data = resp.json()
        media_url: str = data["url"]
    except Exception as e:
        logger.error(f"解析表情包响应数据失败: {e}")
        raise NetworkError("解析表情包接口数据失败") from e

    try:
        media_resp = await client.get(media_url)
        media_resp.raise_for_status()
        return media_resp.content
    except httpx.HTTPStatusError as e:
        logger.error(f"下载表情包图片响应状态异常: {e.response.status_code}")
        raise NetworkError(f"下载表情包图片失败: {e.response.status_code}") from e
    except httpx.RequestError as e:
        logger.error(f"下载表情包图片失败: {e}")
        raise NetworkError(f"下载表情包图片异常: {e}") from e
