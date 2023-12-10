import os

# from flask import request, jsonify, render_template

from fastapi.templating import Jinja2Templates
from typing import AsyncGenerator

from src.logger import logger
from src.chatgpt import ChatGPT, DALLE
from src.models import OpenAIModel
from src.memory import Memory

OPENAI_API_KEY="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"
ORGANIZATION_ID="org-ZbiWh6oHbybuxLZiipNt7axC"
OPENAI_MODEL_ENGINE="gpt-3.5-turbo"
API_PROXY="https://chatgpt-api-proxy.cc"

SYSTEM_MESSAGE="You are a helpful assistant."

models = OpenAIModel(api_key=OPENAI_API_KEY,
                     organization_id=ORGANIZATION_ID,
                     model_engine=OPENAI_MODEL_ENGINE,
                     base_url=f"{API_PROXY}/v1/")
memory = Memory(system_message=SYSTEM_MESSAGE)
chatgpt = ChatGPT(models, memory)

# dalle = DALLE(models)

# 处理用户点击菜单跳转不同页面

# 使用Jinja2模板
templates = Jinja2Templates(directory="templates")

def index(request):
    return templates.TemplateResponse("index.html", {"request": request})

# def index():
#   return render_template('index.html', active_menu='home')

# def about():
#   return render_template('about.html', active_menu='about')

# def personal():
#   return render_template('personal.html', active_menu='personal')

# 处理聊天消息，流式返回ChatGPT消息
async def chat_completion(message, websocket)-> AsyncGenerator[str, None]:
    user_input = message
    user_id = websocket.client.host;
    response = await chatgpt.get_response(user_id, user_input)
    role = ""
    all_content = ""
    state, i =['$START.','$END.'], 1
    async for chunk in response:
        role = chunk.choices[0].delta.role if chunk.choices[0].delta.role != role and chunk.choices[0].delta.role is not None else role
        content = chunk.choices[0].delta.content
        if content:
            all_content += content
            yield content
        else:
            i += 1
            yield state[i % 2]
    await chatgpt.memory.append(user_id, {'role': role, 'content': all_content})

# 处理聊天界面用户交互
# def send_message():
#   try:
#     user_input = request.form['user_input']
#     user_id = request.remote_addr
#     receive = chatgpt.get_response(user_id, user_input)
#     return jsonify({'server_response': receive})
#   except Exception as e:
#     logger.error(f"Error processing message: {e}")
#     return jsonify({
#       'server_response':
#       f'Oops! Something went wrong. \n\nerror message: {e}'
#     })

# def clear_chat():
#   try:
#     user_id = request.remote_addr
#     chatgpt.clean_history(user_id)
#     return jsonify({'server_response': 'Chat history cleared.'})
#   except Exception as e:
#     logger.error(f"Error clearing chat history: {e}")
#     return jsonify({
#       'server_response':
#       f'Oops! Something went wrong. \n\nerror message: {e}'
#     })


# 处理保存用户输入的Key
# def set_openai_key():
#   try:
#     data = request.get_json()
#     api_key = data['openai_api_key']
#     chatgpt.model.set_api_key(api_key)
#     return jsonify({'server_response': 'API Key updated successfully.'})
#   except Exception as e:
#     logger.error(f"Error processing message: {e}")
#     return jsonify({
#       'server_response':
#       f'Oops! Something went wrong. \n\nerror message: {e}'
#     })