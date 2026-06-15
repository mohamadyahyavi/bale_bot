from collections import defaultdict


class MemoryState:

    def __init__(self):
        self.store = defaultdict(dict)


    def set(self, user_id: str, key: str, value):
        self.store[user_id][key] = value


    def get(self, user_id: str, key: str, default=None):
        return self.store[user_id].get(key, default)


    def clear(self, user_id: str):
        self.store.pop(user_id, None)