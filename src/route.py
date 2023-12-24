import json
import asyncio
from typing import NoReturn
from fastapi import FastAPI, Request, WebSocket, HTTPException, Form, WebSocketDisconnect
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse
from datetime import datetime, timedelta

from src.views import chat_index, chat_completion, chat_clear, chat_set_key, signin, signup, signout, saveuserinf

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/")
async def index(request: Request):
  return chat_index(request)

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket) -> NoReturn:
    await websocket.accept()
    while True:
        try:
            question = await websocket.receive_json()
        except WebSocketDisconnect:
            # 处理连接断开的情况
            break
        
        async for text in chat_completion(question, websocket):
            await websocket.send_text(text)

        # 发送心跳消息，保持连接活跃
        await websocket.send_text("ping")

        # 设置一个合理的间隔时间，避免过于频繁发送心跳消息
        await asyncio.sleep(30)  # 例如，每30秒发送一次心跳消息


def get_client_ip(request: Request):
    return request.client.host

@app.post("/signup")
async def register(request: Request, username: str = Form(...), email: str = Form(...), password: str = Form(...)):
    # 注册
    try:
      client_ip = get_client_ip(request)
      user = await signup(name=username, email=email, password=password, ip_address=client_ip)
      return JSONResponse(status_code=200, content={"message": "登录成功", "user": user.to_dict()})
    except Exception as e:
      return JSONResponse(status_code=400, content={"message": f"{e}"})

@app.post("/signin")
async def login(request: Request, username: str = Form(...), password: str = Form(...)):
    try:
      client_ip = request.client.host
      user = await signin(name=username, password=password, ip_address=client_ip)
      return JSONResponse(status_code=200, content={"message": "登录成功", "user": user.to_dict()})
    except Exception as e:
      return JSONResponse(status_code=400, content={"message": f"{e}"})

@app.post("/signout")
async def exit(request: Request, username: str = Form(...)):
    await signout(username)
    return JSONResponse(status_code=200, content={"message": "成功退出"})

@app.post("/clear_chat")
async def clear_chat(request: Request):
  return await chat_clear(request)

@app.post("/set_key")
async def set_key(data: dict):
  return await chat_set_key(data)

@app.post("/saveuserinf")
async def updatauserinf(request: Request, username: str = Form(...), key: str = Form(...), proxy: str = Form(...), model: str = Form(...)):
  await saveuserinf(username, key, proxy, model)
  return JSONResponse(status_code=200, content={"message": "更新成功"})