import os

from typing import AsyncGenerator
from fastapi.templating import Jinja2Templates
from fastapi.responses import JSONResponse

from src.logger import logger
from src.chatgpt import ChatGPT, DALLE
from src.models import OpenAIModel
from src.memory import Memory

OPENAI_API_KEY = os.environ['OPENAI_API_KEY'] 
ORGANIZATION_ID = os.environ['ORGANIZATION_ID'] 
OPENAI_MODEL_ENGINE = os.environ['OPENAI_MODEL_ENGINE']
OPENAI_API_PROXY = os.environ.get('OPENAI_API_PROXY', None)
OPENAI_API_PROXY = OPENAI_API_PROXY + "/v1/" if OPENAI_API_PROXY is not None else None

models = OpenAIModel(api_key=OPENAI_API_KEY,
                     organization_id=ORGANIZATION_ID,
                     model_engine=OPENAI_MODEL_ENGINE,
                     base_url=OPENAI_API_PROXY)

memory = Memory(system_message="You are a helpful assistant.")
chatgpt = ChatGPT(models, memory)

# dalle = DALLE(models)

# 使用Jinja2模板
templates = Jinja2Templates(directory="templates")


def chat_index(request):
  return templates.TemplateResponse("index.html", {"request": request})


def chat_about(request):
  return templates.TemplateResponse("about.html", {"request": request})


# 处理聊天消息，流式返回ChatGPT消息
async def chat_completion(message, websocket) -> AsyncGenerator[str, None]:
  user_input = message
  user_id = websocket.client.host
  print("user message's", message)
  response = await chatgpt.get_response(user_id, user_input)
  role = ""
  all_content = ""
  state, i = ['$START.', '$END.'], 1
  async for chunk in response:
    role = chunk.choices[
        0].delta.role if chunk.choices[0].delta.role != role and chunk.choices[
            0].delta.role is not None else role
    content = chunk.choices[0].delta.content
    if content:
      all_content += content
      yield content
    else:
      i += 1
      yield state[i % 2]
  await chatgpt.memory.append(user_id, {'role': role, 'content': all_content})


async def chat_clear(request):
  try:
    user_id = request.client.host
    await chatgpt.clean_history(user_id)

    return JSONResponse(content={'server_response': 'Chat history cleared.'})
  except Exception as e:
    logger.error(f"Error clearing chat history: {e}")
    return JSONResponse(
        status_code=500,
        content={
            'server_response':
            f'Oops! Something went wrong. \n\nerror message: {e}'
        })


# 处理保存用户输入的Key
async def chat_set_key(data):
  try:
    api_key = data['openai_api_key']
    api_proxy = data['openai_api_proxy']

    print("save key and proxy: ", api_key, api_proxy)

    # 假设 chatgpt 和 chatgpt.model 已经在其他地方正确初始化
    chatgpt.model.set_api_key(api_key)
    chatgpt.model.set_api_proxy(api_proxy)
    return {'server_response': 'API Key and Proxy updated successfully.'}
  except Exception as e:
    # 你可以使用 FastAPI 的 HTTPException 来返回带有错误信息的 HTTP 响应
    raise JSONResponse(
        status_code=500,
        content={
            'server_response':
            f'Oops! Something went wrong. \n\nerror message: {e}'
        })
