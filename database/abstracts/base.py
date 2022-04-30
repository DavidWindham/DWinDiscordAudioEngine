from abc import ABC, abstractmethod


class DB(ABC):
    @abstractmethod
    def connect(self):
        pass

    @abstractmethod
    def add_server(self, server_id: int) -> None:
        pass

    @abstractmethod
    def update_server_info(self, server_id: int, queue_message_id: int, history: list):
        pass

    @abstractmethod
    def load_all_server_info(self):
        pass

    @abstractmethod
    def load_single_server_info(self, server_id: int):
        pass

    @abstractmethod
    def add_item_to_server_history(self, server_id: int, item_to_add: dict):
        pass

    @abstractmethod
    def get_server_history(self, server_id: int, limit: int) -> list:
        pass

    @abstractmethod
    def get_queue_message_id(self, server_id: int) -> int or None:
        pass

    @abstractmethod
    def set_queue_message_id(self, server_id: int, queue_message_id: int):
        pass
