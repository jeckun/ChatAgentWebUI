from typing import NoReturn
from fastapi import FastAPI, Request, WebSocket
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from src.views import chat_index, chat_completion, chat_clear, chat_set_key

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")


# 使用Jinja2模板
templates = Jinja2Templates(directory="templates")


@app.get("/")
async def index(request: Request):
  return chat_index(request)

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket) -> NoReturn:
  await websocket.accept()
  while True:
    question = await websocket.receive_text()
    async for text in chat_completion(question, websocket):
      await websocket.send_text(text)


@app.post("/clear_chat")
async def clear_chat(request: Request):
  return await chat_clear(request)


@app.post("/set_key")
async def set_key(data: dict):
  return await chat_set_key(data)
