from typing import NoReturn
from fastapi import FastAPI, Request, WebSocket, HTTPException, Form
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from src.views import chat_index, chat_completion, chat_clear, chat_set_key, signin, signup

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")


# 使用Jinja2模板
templates = Jinja2Templates(directory="templates")


@app.get("/")
async def index(request: Request):
  return chat_index(request)


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket) -> NoReturn:
  # 与ChatGPT对话
  await websocket.accept()
  while True:
    question = await websocket.receive_text()
    async for text in chat_completion(question, websocket):
      await websocket.send_text(text)


def get_client_ip(request: Request):
    return request.client.host

@app.post("/signup")
async def register(request: Request, username: str = Form(...), email: str = Form(...), password: str = Form(...)):
    # 注册
    client_ip = get_client_ip(request)
    valimsg = signup(name=username, email=email, password=password, ip_address=client_ip)
    if valimsg:
        raise HTTPException(status_code=400, detail="Username already registered")
    return {"message": "User registered successfully", "user": str(valimsg['user'])}

@app.post("/signin")
async def login(request: Request, username: str = Form(...), email: str = Form(...), password: str = Form(...)):
    # 登录
    client_ip = get_client_ip(request)
    print("login", username)
    valimsg = signin(name=username, email=email, password=password, ip_address=client_ip)
    if valimsg:
        raise HTTPException(status_code=400, detail="Username already registered")
    return {"message": "User logined successfully", "user": str(valimsg['user'])}

@app.post("/clear_chat")
async def clear_chat(request: Request):
  return await chat_clear(request)


@app.post("/set_key")
async def set_key(data: dict):
  return await chat_set_key(data)
