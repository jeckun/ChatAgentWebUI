from src.models import ModelInterface
from src.memory import MemoryInterface


class ChatGPT:
    def __init__(self, model: ModelInterface, memory: MemoryInterface):
        self.model = model
        self.memory = memory

    # 流式响应，处理发给用户的消息
    async def get_response(self, currentSession):
        return await self.model.chat_completion(await currentSession.getMessage())
    
    async def clean_history(self, user_id: str) -> None:
        await self.memory.remove(user_id)


class DALLE:
    def __init__(self, model: ModelInterface):
        self.model = model

    def generate(self, text: str) -> str:
        return self.model.image_generation(text)