from typing import Dict
from collections import defaultdict, deque


class MemoryInterface:
    def append(self, user_id: str, message: Dict) -> None:
        pass

    def get(self, user_id: str) -> str:
        return ""

    def remove(self, user_id: str) -> None:
        pass


class Memory(MemoryInterface):
    def __init__(self, system_message, max_history=10):
        self.storage = defaultdict(deque)        # 使用先进先出队列（FIFO）处理历史对话记录过长的问题
        self.system_message = system_message
        self.max_history = max_history

    def initialize(self, user_id: str):
        self.storage[user_id] = deque([{
            'role': 'system', 'content': self.system_message
        }], maxlen=self.max_history)

    def append(self, user_id: str, message: Dict) -> None:
        if not self.storage[user_id]:
            self.initialize(user_id)
        self.storage[user_id].append(message)

    def get(self, user_id: str) -> str:
        return list(self.storage[user_id])

    def remove(self, user_id: str) -> None:
        self.storage[user_id].clear()
