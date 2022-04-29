from abc import ABC, abstractmethod


class ServerDBComm(ABC):
    def __init__(self, db, server_id):
        self.db = db
        self.server_id = server_id

    @abstractmethod
    def get_queue_message_id(self) -> int or None:
        pass

    @abstractmethod
    def set_queue_message_id(self, queue_message_id: int):
        pass

    @abstractmethod
    def get_history(self, limit: int = 10) -> list:
        pass

    @abstractmethod
    def append_to_history(self, item_to_add: dict):
        pass
