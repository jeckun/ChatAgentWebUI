from typing import Dict
from collections import defaultdict, deque

class MemoryInterface:
    async def append(self, user_id: str, message: Dict) -> None:
        pass

    async def get(self, user_id: str) -> str:
        return ""

    async def remove(self, user_id: str) -> None:
        pass

# 改为支持异步读写的FIFO队列，读写memory对象时需要加 await。
class Memory(MemoryInterface):
    def __init__(self, system_message, max_history=10):
        self.storage = defaultdict(deque)
        self.system_message = system_message
        self.max_history = max_history

    def initialize(self, user_id: str):
        self.storage[user_id] = deque([{
            'role': 'system', 'content': self.system_message
        }], maxlen=self.max_history)

    async def append(self, user_id: str, message: Dict) -> None:
        if not self.storage[user_id]:
            self.initialize(user_id)
        self.storage[user_id].append(message)

    async def get(self, user_id: str) -> str:
        return list(self.storage[user_id])

    async def remove(self, user_id: str) -> None:
        self.storage[user_id].clear()
