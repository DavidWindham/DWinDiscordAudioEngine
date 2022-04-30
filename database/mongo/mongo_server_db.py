class MongoServerObject:
    def __init__(self, db, server_id):
        self.db = db
        self.server_id = server_id

    def get_queue_message_id(self) -> int or None:
        return None

    def set_queue_message_id(self, queue_message_id: int):
        pass

    def get_history(self, limit: int = 10):
        pass

    def append_to_history(self, item_to_add: dict):
        pass
