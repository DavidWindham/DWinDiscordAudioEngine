from db.abstracts.server_db_base import ServerDBComm


class ServerDB(ServerDBComm):
    def __init__(self, db, server_id):
        self.db = db
        self.server_id = server_id

    def get_queue_message_id(self) -> int or None:
        return self.db.get_queue_message_id(server_id=self.server_id)

    def set_queue_message_id(self, queue_message_id: int):
        return self.db.set_queue_message_id(server_id=self.server_id, queue_message_id=queue_message_id)

    def get_history(self, limit: int = 10) -> list:
        return self.db.get_server_history(server_id=self.server_id)

    def append_to_history(self, item_to_add: dict):
        return self.db.add_item_to_server_history(server_id=self.server_id, item_to_add=item_to_add)
