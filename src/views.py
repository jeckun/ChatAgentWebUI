import os
from flask import request, jsonify, render_template

from src.logger import logger
from src.chatgpt import ChatGPT, DALLE
from src.models import OpenAIModel
from src.memory import Memory

models = OpenAIModel(api_key=os.environ['OPENAI_API_KEY'],
                     model_engine=os.environ['OPENAI_MODEL_ENGINE'])
memory = Memory(system_message=os.getenv('SYSTEM_MESSAGE'))
chatgpt = ChatGPT(models, memory)
dalle = DALLE(models)


# 添加根路由，用于加载 index.html 页面
def index():
  return render_template('index.html', active_menu='home')

def about():
  return render_template('about.html', active_menu='about')

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
