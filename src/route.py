from typing import NoReturn
from fastapi import FastAPI, Request, WebSocket
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from src.views import chat_completion

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static") 

# 使用Jinja2模板
templates = Jinja2Templates(directory="templates")

@app.get("/")
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket) -> NoReturn:
    """
    Websocket for AI responses
    """
    await websocket.accept()
    while True:
        question = await websocket.receive_text()
        async for text in chat_completion(question, websocket):
            await websocket.send_text(text)
