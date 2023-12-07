from flask import Flask
# from fastapi import FastAPI, Request
import src.views as views

app = Flask('ChatGPT-Bot')
# app = FastAPI()

# @app.get('/')
# async def home(request: Request):
#     return views.index(request)

# @app.get('/about')
# async def about(request: Request):
#     return views.about(request)

# @app.get('/personal')
# async def personal(request: Request):
#     return views.personal(request)

app.add_url_rule('/', 'home', views.index)
app.add_url_rule('/about', 'about', views.about)
app.add_url_rule('/personal', 'personal', views.personal)
app.add_url_rule('/send_message', 'send_message', views.send_message, methods=['POST'])
app.add_url_rule('/set_key', 'set_key', views.set_openai_key, methods=['POST'])
app.add_url_rule('/clear_chat', 'clear_chat', views.clear_chat, methods=['POST'])
