<!-- markdownlint-disable MD033 MD036 MD041 -->

<div align="center">

<a href="https://v2.nonebot.dev/store">
  <img src="https://raw.githubusercontent.com/A-kirami/nonebot-plugin-template/resources/nbp_logo.png" width="180" height="180" alt="NoneBotPluginLogo">
</a>

<p>
  <img src="https://raw.githubusercontent.com/lgc-NB2Dev/readme/main/template/plugin.svg" alt="NoneBotPluginText">
</p>

# nonebot-plugin-wuwa-emoji

_✨ 鸣潮表情包插件 ✨_

![License](https://img.shields.io/github/license/lyqgzbl/nonebot-plugin-wuwa-emoji.svg)
![PyPI](https://img.shields.io/pypi/v/nonebot-plugin-wuwa-emoji.svg)
![Python](https://img.shields.io/badge/python-3.10+-blue.svg)
[![NoneBot Registry](https://img.shields.io/endpoint?url=https%3A%2F%2Fnbbdg.lgc2333.top%2Fplugin%2Fnonebot-plugin-wuwa-emoji)](https://registry.nonebot.dev/plugin/nonebot-plugin-wuwa-emoji:nonebot_plugin_wuwa_emoji)
[![Supported Adapters](https://img.shields.io/endpoint?url=https%3A%2F%2Fnbbdg.lgc2333.top%2Fplugin-adapters%2Fnonebot-plugin-alconna)](https://registry.nonebot.dev/plugin/nonebot-plugin-alconna:nonebot_plugin_alconna)

</div>

## 安装

使用 nb-cli [推荐]
```shell
nb plugin install nonebot-plugin-wuwa-emoji
```

使用 pip
```shell
pip install nonebot-plugin-wuwa-emoji
```

使用 uv
```shell
uv add nonebot-plugin-wuwa-emoji
```

## 使用

命令需要加 [NoneBot 命令前缀](https://nonebot.dev/docs/appendices/config#command-start-和-command-separator) (默认为`/`)

使用命令 `鸣潮表情包` 触发插件：
- `/鸣潮表情包` 随机获取一张鸣潮表情包
- `/鸣潮表情包 [角色名]` 随机获取指定角色的鸣潮表情包（例如：`/鸣潮表情包 秧秧`、`/鸣潮表情包 爱弥斯`）

## 配置项

配置方式：直接在 NoneBot 全局配置文件中添加以下配置项即可

### wuwa_emoji_token [必填]

- 类型：`str`
- 默认值：`None`
- 说明：用于请求 [鸣潮表情包站](https://emoji.wuwa.games/) 随机表情包接口的 API Token
