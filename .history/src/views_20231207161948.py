import os
from flask import request, jsonify, render_template

# from fastapi import HTTPException
# from fastapi.templating import Jinja2Templates

from src.logger import logger
from src.chatgpt import ChatGPT, DALLE
from src.models import OpenAIModel
from src.memory import Memory

OPENAI_API_KEY="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"
# ORGANIZATION_ID="org-ZbiWh6oHbybuxLZiipNt7axC"
ORGANIZATION_ID=""
OPENAI_MODEL_ENGINE="gpt-3.5-turbo"
SYSTEM_MESSAGE="You are a helpful assistant."
PROXY="https://chatgpt-api-proxy.cc/v1/"

models = OpenAIModel(api_key=OPENAI_API_KEY,
                     organization_id=ORGANIZATION_ID,
                     model_engine=OPENAI_MODEL_ENGINE,
                     proxy=PROXY)
memory = Memory(system_message=SYSTEM_MESSAGE)
chatgpt = ChatGPT(models, memory)
dalle = DALLE(models)

# 初始化 Jinja2 模板引擎
# templates = Jinja2Templates(directory="templates")

# 处理用户点击菜单跳转不同页面
def index():
  return render_template('index.html', active_menu='home')

def about():
  return render_template('about.html', active_menu='about')
  # return templates.TemplateResponse("index.html", {"request": request, "active_menu": "about"})

def personal():
  return render_template('personal.html', active_menu='personal')
  # return templates.TemplateResponse("index.html", {"request": request, "active_menu": "personal"})

# 处理聊天界面用户交互
def send_message():
  try:
    user_input = request.form['user_input']
    user_id = request.remote_addr
    receive = chatgpt.get_response(user_id, user_input)
    return jsonify({'server_response': receive})
  except Exception as e:
    logger.error(f"Error processing message: {e}")
    return jsonify({
      'server_response':
      f'Oops! Something went wrong. \n\nerror message: {e}'
    })

def clear_chat():
  try:
    user_id = request.remote_addr
    chatgpt.clean_history(user_id)
    return jsonify({'server_response': 'Chat history cleared.'})
  except Exception as e:
    logger.error(f"Error clearing chat history: {e}")
    return jsonify({
      'server_response':
      f'Oops! Something went wrong. \n\nerror message: {e}'
    })


# 处理保存用户输入的Key
def set_openai_key():
  try:
    data = request.get_json()
    api_key = data['openai_api_key']
    chatgpt.model.set_api_key(api_key)
    return jsonify({'server_response': 'API Key updated successfully.'})
  except Exception as e:
    logger.error(f"Error processing message: {e}")
    return jsonify({
      'server_response':
      f'Oops! Something went wrong. \n\nerror message: {e}'
    })