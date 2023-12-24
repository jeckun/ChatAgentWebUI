import openai
from openai import AsyncOpenAI
from openai._streaming import AsyncStream
from typing import List, Dict


class ModelInterface:

  async def chat_completion(self, messages: List[Dict]) -> str:
    pass

  def image_generation(self, prompt: str) -> str:
    pass


class OpenAIModel(ModelInterface):

  def __init__(self,
               api_key: str,
               model_engine: str,
               organization_id: str | None = None,
               base_url: str | None = None,
               image_size: str = '512x512'):
    self.client = AsyncOpenAI(api_key=api_key,
                              organization=organization_id,
                              base_url=base_url)
    self.model_engine = model_engine
    self.image_size = image_size

  # 与ChatGPT进行聊天，返回ChatGPT消息
  async def chat_completion(self, messages) -> AsyncStream:
    return await self.client.chat.completions.create(
        model=self.model_engine,
        messages=messages,
        stream=True,
    )

  def set_api_key(self, api_key: str):
    self.client.api_key = api_key

  def set_api_proxy(self, api_proxy: str | None = None):
    self.client.base_url = api_proxy

  def set_model_engine(self, moel_engine: str):
    self.model_engine = moel_engine

  def set_image_size(self, image_size: str = '512x512'):
    self.image_size = image_size

  def image_generation(self, prompt: str) -> str:
    response = openai.Image.create(prompt=prompt, n=1, size=self.image_size)
    image_url = response.data[0].url
    return image_url
