# from flask import Flask
# import src.views as views

# app = Flask('ChatGPT-Bot')

# app.add_url_rule('/', 'home', views.index)
# app.add_url_rule('/about', 'about', views.about)
# app.add_url_rule('/personal', 'personal', views.personal)
# app.add_url_rule('/send_message', 'send_message', views.send_message, methods=['POST'])
# app.add_url_rule('/set_key', 'set_key', views.set_openai_key, methods=['POST'])
# app.add_url_rule('/clear_chat', 'clear_chat', views.clear_chat, methods=['POST'])

from typing import NoReturn
from fastapi import FastAPI, Request, WebSocket
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse

from src.views import index, chat_completion

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static") 


# @app.get("/", response_class=HTMLResponse)
# async def web_app():
#     return await index()

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
