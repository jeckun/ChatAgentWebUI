# ChatGPT Bot in Python

## 关于

用Python+Flask写的ChatGPT聊天机器人，已经在Replit上部署，想要试试的可以直接使用。

Demo： https://replit.com/@jeckun9527/ChatBot-in-Python?v=1

## 使用前提

你必须有一个OpenAi的账号，然后访问下列网址，自己创建一个Key，复制保存好，在设置中粘贴保存即可。

API Key 获取地址： https://platform.openai.com/api-keys

## 开发计划

1、制作 Dorker 镜像，实现一键部署。   ——  完成

2、增加国内使用的 ChatGPT API Proxy，实现在国内用户快速部署与使用。  —— 完成

3、实现流式输出，将服务端消息一个一个传回来，就像 ChatGPT 自己的聊天方式一样。由于Flask不支持异步传输，准备将Flask换成FastApi。

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

## Effect

![效果图](https://github.com/jeckun/ChatGPT-bot-in-python/blob/main/static/img/2566-11-30-20.29.55.webp)

![效果图](https://github.com/jeckun/ChatGPT-bot-in-python/blob/main/static/img/2566-11-30-20.30.24.webp)

```html
<video autoplay loop>
<source src="https://github.com/jeckun/ChatGPT-bot-in-python/blob/main/static/video/stream-chat-video.mp4" type="video/mp4">
您的浏览器不支持HTML5视频标签。
</video>
```

```HTML
<video width="720" height="303" controls> 
<source src="https://github.com/jeckun/ChatGPT-bot-in-python/blob/main/static/video/stream-chat-video.mp4" type="video/mp4">
</video>
```
