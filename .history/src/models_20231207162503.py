from typing import List, Dict
import openai
from openai import OpenAI


class ModelInterface:

  def chat_completion(self, messages: List[Dict]) -> str:
    pass

  def image_generation(self, prompt: str) -> str:
    pass


class OpenAIModel(ModelInterface):

  def __init__(self,
               api_key: str,
               organization_id: str,
               model_engine: str,
               proxy: str = '',
               image_size: str = '512x512'):
      self.client = OpenAI(
          api_key=api_key,
          organization=organization_id,
          base_url=proxy
      )
      self.model_engine = model_engine
      self.image_size = image_size

  def set_api_key(self, api_key: str) -> None:
    # openai.api_key = api_key
      self.client.api_key = api_key

  def set_model_engine(self, moel_engine: str) -> None:
    self.model_engine = moel_engine

  def set_image_size(self, image_size: str = '512x512') -> None:
    self.image_size = image_size

  def chat_completion(self, messages) -> str:
    response = self.client.chat.completions.create(
      model=self.model_engine,
      messages=messages,
      stream=None)
    return response

  def image_generation(self, prompt: str) -> str:
    response = openai.Image.create(prompt=prompt, n=1, size=self.image_size)
    image_url = response.data[0].url
    return image_url
