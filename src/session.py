from src.chatgpt import ChatGPT
from src.models import OpenAIModel
from src.memory import Memory
from src.user import User
import random

class Session:
    def __init__(self, user, ip_address, sessionData = None):
        # Extracting session information
        self.id = 0
        self._user = user
        self.ip_address = ip_address
        self.memory = None
        self.apiKey = user.current_key
        self.model = user.default_model
        self.proxy = user.proxy_url

        self.id = random.randint(100000, 999999)
        if sessionData:
            sessionInfo = sessionData[list(sessionData.keys())[0]]
            self.title = sessionInfo.get("title", "None")
            self.proxy = sessionInfo.get("proxy", "")
            self.model = sessionInfo.get("model", "")
            self.apiKey = sessionInfo.get("apiKey", "")
            self.chatRounds = sessionInfo.get("chatRounds", 0)
            self.totalToken = sessionInfo.get("totalToken", 0)

        if not self._user:
            self._user = User.login(sessionInfo.get("user"), sessionInfo.get('password'))

        # Creating OpenAIModel object
        models = OpenAIModel(api_key=self.apiKey, model_engine=self.model, base_url=self.proxy)
        self.chatgpt = ChatGPT(models, self.memory)

    @property
    def user(self):
        return self._user
    
    @user.setter
    def user(self, value):
        self._user = value
        self.proxy = self._user.proxy_url
        self.model = self._user.default_model
        self.apiKey = self._user.current_key
        self.chatgpt.model.set_api_key(self.apiKey)
        self.chatgpt.model.set_api_proxy(self.proxy)
        self.chatgpt.model.set_model_engine(self.model)

    async def appendMessage(self, messages):
        for message in messages:
            if 'system' in message:
                self.memory = Memory(message['system'])
            elif 'user' in message:
                await self.memory.append(self.ip_address + '-' + str(self.user.id), {'role': 'user', 'content': message['user']})
            elif 'assistant' in message:
                await self.memory.append(self.ip_address + '-' + str(self.user.id), {'role': 'assistant', 'content': message['assistant']})

    async def getMessage(self):
        return await self.memory.get(self.ip_address + '-' +str(self.user.id))