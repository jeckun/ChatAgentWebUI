import os

from typing import AsyncGenerator
from fastapi.templating import Jinja2Templates
from fastapi.responses import JSONResponse

from src.logger import logger
from src.chatgpt import ChatGPT, DALLE
from src.models import OpenAIModel
from src.memory import Memory
from src.user import User
from src.session import Session

OPENAI_API_KEY = os.environ['OPENAI_API_KEY'] 
OPENAI_MODEL_ENGINE = os.environ['OPENAI_MODEL_ENGINE']
OPENAI_API_PROXY = os.environ.get('OPENAI_API_PROXY', None)
OPENAI_API_PROXY = OPENAI_API_PROXY + "/v1/" if OPENAI_API_PROXY is not None else None

models = OpenAIModel(
    api_key=OPENAI_API_KEY,
    model_engine=OPENAI_MODEL_ENGINE,
    base_url=OPENAI_API_PROXY
    )

memory = Memory(system_message="You are a helpful assistant.")
chatgpt = ChatGPT(models, memory)
currentUsers = {}
currentSession = None

# dalle = DALLE(models)

# 使用Jinja2模板
templates = Jinja2Templates(directory="templates")


# 加载聊天首页
def chat_index(request):
    return templates.TemplateResponse("index.html", {"request": request})


# 处理聊天消息，流式返回ChatGPT消息
async def chat_completion(message, websocket) -> AsyncGenerator[str, None]:
    try:
        user_ip = websocket.client.host
        global currentSession
        # 启动新的会话
        if (list(message.keys())[0]=='999999'):
            currentSession = Session(currentUsers, message, user_ip)
        messages = message[list(message.keys())[0]].get("messages", [])
        await currentSession.appendMessage(messages)
        
        response = await currentSession.chatgpt.get_response(currentSession)
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
        await currentSession.appendMessage([{'assistant': all_content}])
    except Exception as e:
        await websocket.send_text(f"Oops! Something went wrong. \n\n {e}")

async def signin(name, password, ip_address: str | None = None):
    global currentSession
    # 登录
    user = User.login(name, password, ip_address)
    currentUsers[user.name]=user
    currentSession = Session(user, ip_address)
    return user

async def signup(name, password, email, ip_address: str | None = None):
    global currentSession
    # 注册
    user = User.register(name,password,email,ip_address)
    currentUsers[user.name]=user
    currentSession = Session(user, ip_address)
    return user

async def signout(name):
    global currentSession
    # 退出
    del currentUsers[name]
    currentSession = None

async def saveuserinf(name, key, proxy, model):
    global currentSession
    # 更新
    user = User.query(username=name)
    user = User.login(name=user[0]['name'], password=user[0]['password'])
    user.current_key = key
    user.proxy_url = proxy
    user.default_model = model
    user.save()
    currentSession.user = user


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
