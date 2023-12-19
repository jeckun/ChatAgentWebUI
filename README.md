# ChatGPT Bot in Python

## 关于

这是一个个人实践项目，使用 OpenAI 的 GPT-3 模型创建的聊天机器人。 如果您有兴趣，请随时提出问题，请求您感兴趣的其他功能，或者加入我们一起改进它。

Demo： https://replit.com/@jeckun9527/ChatBot-in-Python?v=1

## 使用前提

你必须有一个OpenAi的账号，然后访问下列网址，自己创建一个Key，复制保存好，在设置中粘贴保存即可。

API Key 获取地址： https://platform.openai.com/api-keys

## 注册代理

想在国内使用，要么科学上网，要么使用代理。使用别人的代理不放心的话，可以自己搭建一个，具体方法如下。

[ChatGPTProxyAPI](https://github.com/x-dr/chatgptProxyAPI)

## 实现功能

1. 使用最新 OpenAI 1.3.7 API接口，与旧版接口有些不同，已对部分聊天代码进行了迁移，后面继续完善其他的代码；

2. 可自行设置代理地址，实现在国内部署与使用；

3. 上下文保持，每次对话都会保留最近几次聊天内容回传 GPT，让他的回答更加准确；

4. 用 WebSocket + JavaScript 实现流式输出，可以像官方 ChatGPT 一样，分段返回答案。改善了用户体验；

5. 前端配置 key 和 代理；

## 遇到的问题

1. 请不要泄露你的Key，否则官方可能会直接删除它。如果遇到，需要再生成一个Key。
2. 部署到正式环境时，使用 https 可能会遇 wss 连接断开的问题，最新代码已经解决此问题。

## 修改代理

想使用自己的代理服务器，可以修改 views.py 中的 PROXY.

```
PROXY="【换成你自己的代理服务器网址】/v1/"
```

## 发布更新

2023-11-30 在 Replit 上首次发布

2023-12-04 解决一次多次会话后会Token超过限制的问题。

2023-12-07 实现 ChatGPT API Proxy ，可以部署在国内了。实现OpenAi==1.3.7接口。

2023-12-10 实现流式对话，用户能够更快的看到 ChatGPT 回复消息，提升了用户体验。为了实现这个流式对话，替换了不能异步通信的Flask，改为使用FastAPI。

2023-12-19 更新界面，同时修复ws连接错误。

## About

This is a chatbot that uses OpenAI's GPT-3 language model to generate responses.

## Premise

Please set your OpenAI's API keys first.

## Plan

1. Biuld Dorker image
2. Add ChatGPT API Proxy

## Log

2023-11-30 Published and The issue of invalid storage of OpenAI API keys has been resolved.

2023-12-04 Resolved the issue of token exceeding the limit after multiple sessions in a single interaction.

2023-12-07 Implemented ChatGPT API Proxy, now deployable in China. Upgraded to OpenAI 1.3.7.

2023-12-10 implemented streaming conversations to allow users to see ChatGPT reply messages more quickly, enhancing the user experience. To achieve this streaming dialogue, Flask, which does not support asynchronous communication, was replaced with FastAPI.

2023-12-19 Update the WebUI and fix the ws connection error.

## Effect

![效果图](https://github.com/jeckun/ChatShare/blob/ChatShare-0-0-005/doc/2023-12-19_12.51.28.webp)

https://github.com/jeckun/ChatGPT-bot-in-python/assets/31623221/7b95574c-4b8e-4868-a99f-8693632440f4
