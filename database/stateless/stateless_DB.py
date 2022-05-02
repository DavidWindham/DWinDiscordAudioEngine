from ..abstracts.base import DB


class StatelessDB(DB):
    def connect(self):
        pass

    def add_server(self, server_id: int) -> None:
        pass

    def update_server_info(self, server_id: int, queue_message_id: int, history: list):
        pass

    def load_all_server_info(self):
        return []

    def load_single_server_info(self, server_id: int):
        return None

    def add_item_to_server_history(self, server_id: int, item_to_add: dict):
        pass

    def get_server_history(self, server_id: int, limit: int) -> list:
        return []

    def get_queue_message_id(self, server_id: int) -> int or None:
        return None

    def set_queue_message_id(self, server_id: int, queue_message_id: int):
        pass
